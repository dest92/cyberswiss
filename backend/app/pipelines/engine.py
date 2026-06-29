import asyncio
import uuid
from datetime import datetime, timezone

import dramatiq

from app.core.config import settings
from app.db.session import SessionLocal
from app.models.job import Job, JobStatus
from app.models.pipeline_run import PipelineRun, PipelineRunStatus
from app.pipelines.definitions import get_pipeline
from app.tools.base import NormalizedResult
from app.workers.actors import _execute_job
from app.workers.broker import redis_broker  # noqa: F401  (configures the dramatiq broker)


async def _run_pipeline_async(pipeline_run_id: str) -> None:
    async with SessionLocal() as db:
        run = await db.get(PipelineRun, uuid.UUID(pipeline_run_id))
        if run is None:
            return

        definition = get_pipeline(run.pipeline_name)
        run.status = PipelineRunStatus.running
        run.started_at = datetime.now(timezone.utc)
        await db.commit()

        previous_results: list[NormalizedResult] = []
        for index, step in enumerate(definition.steps):
            params = step.build_params(run.params, previous_results)
            job = Job(
                engagement_id=run.engagement_id,
                pipeline_run_id=run.id,
                step_index=index,
                tool_name=step.tool_name,
                params=params,
            )
            db.add(job)
            await db.commit()

            previous_results = await _execute_job(db, job)

            if job.status != JobStatus.success:
                run.status = PipelineRunStatus.failed
                run.error_message = (
                    f"paso {index} ({step.tool_name}) terminó en estado "
                    f"'{job.status.value}': {job.error_message or 'sin detalle'}"
                )
                run.finished_at = datetime.now(timezone.utc)
                await db.commit()
                return

        run.status = PipelineRunStatus.success
        run.finished_at = datetime.now(timezone.utc)
        await db.commit()


@dramatiq.actor(max_retries=0, time_limit=settings.job_default_timeout_seconds * 1000 * 6 + 60_000)
def run_pipeline(pipeline_run_id: str) -> None:
    asyncio.run(_run_pipeline_async(pipeline_run_id))
