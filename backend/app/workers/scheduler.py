import asyncio
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.job import Job
from app.models.scheduled_scan import ScheduledScan
from app.workers.actors import run_job
from app.workers.broker import redis_broker  # noqa: F401  (configures the dramatiq broker)

logger = logging.getLogger("cyberswiss.scheduler")
POLL_INTERVAL_SECONDS = 30


async def _run_due_scans() -> None:
    now = datetime.now(timezone.utc)
    async with SessionLocal() as db:
        result = await db.execute(
            select(ScheduledScan).where(
                ScheduledScan.enabled.is_(True), ScheduledScan.next_run_at <= now
            )
        )
        due = list(result.scalars().all())
        for scheduled_scan in due:
            job = Job(
                engagement_id=scheduled_scan.engagement_id,
                tool_name=scheduled_scan.tool_name,
                params=scheduled_scan.params,
            )
            db.add(job)
            await db.flush()
            run_job.send(str(job.id))

            scheduled_scan.last_run_at = now
            scheduled_scan.next_run_at = now + timedelta(minutes=scheduled_scan.interval_minutes)
            logger.info(
                "lanzado escaneo recurrente %s (%s) para engagement %s",
                scheduled_scan.id,
                scheduled_scan.tool_name,
                scheduled_scan.engagement_id,
            )
        await db.commit()


async def _loop() -> None:
    logger.info("scheduler de escaneos recurrentes iniciado (poll cada %ss)", POLL_INTERVAL_SECONDS)
    while True:
        try:
            await _run_due_scans()
        except Exception:
            logger.exception("error revisando escaneos recurrentes")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    asyncio.run(_loop())


if __name__ == "__main__":
    main()
