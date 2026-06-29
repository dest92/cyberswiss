import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.pipeline_run import PipelineRun
from app.pipelines.definitions import list_pipelines
from app.pipelines.engine import run_pipeline
from app.schemas.pipeline_run import PipelineRunCreate, PipelineRunOut

catalog_router = APIRouter(
    prefix="/api/pipelines", tags=["pipelines"], dependencies=[Depends(get_current_user)]
)


@catalog_router.get("", response_model=list[str])
async def list_pipeline_definitions() -> list[str]:
    return list_pipelines()


router = APIRouter(
    prefix="/api/engagements/{engagement_id}/pipeline-runs",
    tags=["pipelines"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[PipelineRunOut])
async def list_pipeline_runs(
    engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[PipelineRun]:
    result = await db.execute(
        select(PipelineRun)
        .where(PipelineRun.engagement_id == engagement_id)
        .options(selectinload(PipelineRun.jobs))
        .order_by(PipelineRun.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("", response_model=PipelineRunOut, status_code=status.HTTP_201_CREATED)
async def create_pipeline_run(
    engagement_id: uuid.UUID, payload: PipelineRunCreate, db: AsyncSession = Depends(get_db)
) -> PipelineRun:
    if payload.pipeline_name not in list_pipelines():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Pipeline desconocido: {payload.pipeline_name}",
        )

    run = PipelineRun(
        engagement_id=engagement_id, pipeline_name=payload.pipeline_name, params=payload.params
    )
    db.add(run)
    await db.commit()
    await db.refresh(run, attribute_names=["jobs"])

    run_pipeline.send(str(run.id))
    return run


@router.get("/{pipeline_run_id}", response_model=PipelineRunOut)
async def get_pipeline_run(
    engagement_id: uuid.UUID, pipeline_run_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> PipelineRun:
    result = await db.execute(
        select(PipelineRun)
        .where(PipelineRun.id == pipeline_run_id)
        .options(selectinload(PipelineRun.jobs))
    )
    run = result.scalar_one_or_none()
    if run is None or run.engagement_id != engagement_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Pipeline run no encontrado"
        )
    return run
