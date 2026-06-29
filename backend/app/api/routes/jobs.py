import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.job import Job
from app.schemas.job import JobCreate, JobOut
from app.tools import registry
from app.workers.actors import run_job

router = APIRouter(
    prefix="/api/engagements/{engagement_id}/jobs",
    tags=["jobs"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[JobOut])
async def list_jobs(engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> list[Job]:
    result = await db.execute(
        select(Job).where(Job.engagement_id == engagement_id).order_by(Job.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("", response_model=JobOut, status_code=status.HTTP_201_CREATED)
async def create_job(
    engagement_id: uuid.UUID, payload: JobCreate, db: AsyncSession = Depends(get_db)
) -> Job:
    if payload.tool_name not in registry.list_tools():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Herramienta desconocida: {payload.tool_name}",
        )

    job = Job(engagement_id=engagement_id, tool_name=payload.tool_name, params=payload.params)
    db.add(job)
    await db.commit()
    await db.refresh(job)

    run_job.send(str(job.id))
    return job


@router.get("/{job_id}", response_model=JobOut)
async def get_job(
    engagement_id: uuid.UUID, job_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Job:
    job = await db.get(Job, job_id)
    if job is None or job.engagement_id != engagement_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job no encontrado")
    return job
