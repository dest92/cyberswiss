import asyncio
import uuid
from datetime import datetime, timezone

import dramatiq
from sqlalchemy.dialects.postgresql import insert as pg_insert

from app.core.config import settings
from app.core.docker_runner import DockerToolTimeoutError, run_tool_container
from app.db.session import SessionLocal
from app.models.job import Job, JobStatus
from app.models.target import Target, TargetType
from app.tools import registry
from app.tools.base import NormalizedResult, ResultType
from app.workers.broker import redis_broker  # noqa: F401  (configures the dramatiq broker)


async def _upsert_targets(
    db, engagement_id: uuid.UUID, job_id: uuid.UUID, results: list[NormalizedResult]
) -> None:
    target_types = {ResultType.host: TargetType.host, ResultType.url: TargetType.url}
    rows = [
        {
            "id": uuid.uuid4(),
            "engagement_id": engagement_id,
            "type": target_types[r.type],
            "value": r.value,
            "source_job_id": job_id,
        }
        for r in results
        if r.type in target_types
    ]
    if not rows:
        return
    stmt = pg_insert(Target).values(rows)
    stmt = stmt.on_conflict_do_nothing(constraint="uq_target_identity")
    await db.execute(stmt)


async def _run_job_async(job_id: str) -> None:
    async with SessionLocal() as db:
        job = await db.get(Job, uuid.UUID(job_id))
        if job is None:
            return

        job.status = JobStatus.running
        job.started_at = datetime.now(timezone.utc)
        await db.commit()

        try:
            adapter = registry.get_adapter(job.tool_name)
            command = adapter.build_command(job.params)
            stdin_data = adapter.build_stdin(job.params)

            result = await run_tool_container(
                settings.recon_toolbox_image,
                command,
                stdin_data=stdin_data,
                timeout=job.params.get("timeout_seconds"),
                log_channel=f"job:{job.id}:logs",
            )
        except DockerToolTimeoutError as exc:
            job.status = JobStatus.timeout
            job.error_message = str(exc)
        except Exception as exc:
            job.status = JobStatus.failed
            job.error_message = str(exc)
        else:
            normalized = adapter.parse_output(result.stdout, "")
            job.raw_output = result.stdout
            job.container_id = result.container_id
            job.parsed_results = [r.model_dump(mode="json") for r in normalized]
            job.status = JobStatus.success if result.exit_code == 0 else JobStatus.failed
            await _upsert_targets(db, job.engagement_id, job.id, normalized)

        job.finished_at = datetime.now(timezone.utc)
        await db.commit()


@dramatiq.actor(max_retries=0, time_limit=settings.job_default_timeout_seconds * 1000 + 30_000)
def run_job(job_id: str) -> None:
    asyncio.run(_run_job_async(job_id))
