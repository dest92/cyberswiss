import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.job import Job
from app.models.note import Note
from app.models.report import Report
from app.models.scope import Scope
from app.models.target import Target
from app.schemas.engagement import (
    EngagementCreate,
    EngagementOut,
    EngagementSummary,
    EngagementUpdate,
)

router = APIRouter(
    prefix="/api/engagements", tags=["engagements"], dependencies=[Depends(get_current_user)]
)


@router.get("", response_model=list[EngagementOut])
async def list_engagements(db: AsyncSession = Depends(get_db)) -> list[Engagement]:
    result = await db.execute(select(Engagement).order_by(Engagement.created_at.desc()))
    return list(result.scalars().all())


@router.post("", response_model=EngagementOut, status_code=status.HTTP_201_CREATED)
async def create_engagement(
    payload: EngagementCreate, db: AsyncSession = Depends(get_db)
) -> Engagement:
    engagement = Engagement(**payload.model_dump())
    db.add(engagement)
    await db.commit()
    await db.refresh(engagement)
    return engagement


async def _get_engagement_or_404(engagement_id: uuid.UUID, db: AsyncSession) -> Engagement:
    engagement = await db.get(Engagement, engagement_id)
    if engagement is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Engagement no encontrado")
    return engagement


@router.get("/{engagement_id}", response_model=EngagementOut)
async def get_engagement(engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> Engagement:
    return await _get_engagement_or_404(engagement_id, db)


@router.get("/{engagement_id}/summary", response_model=EngagementSummary)
async def get_engagement_summary(
    engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> EngagementSummary:
    await _get_engagement_or_404(engagement_id, db)

    async def _counts_by(column, model) -> dict[str, int]:
        result = await db.execute(
            select(column, func.count())
            .where(model.engagement_id == engagement_id)
            .group_by(column)
        )
        return {key.value: count for key, count in result.all()}

    async def _total(model) -> int:
        result = await db.execute(
            select(func.count()).where(model.engagement_id == engagement_id)
        )
        return result.scalar_one()

    return EngagementSummary(
        findings_by_severity=await _counts_by(Finding.severity, Finding),
        findings_by_owasp_category=dict(
            (
                await db.execute(
                    select(Finding.owasp_category, func.count())
                    .where(Finding.engagement_id == engagement_id)
                    .group_by(Finding.owasp_category)
                )
            ).all()
        ),
        jobs_by_status=await _counts_by(Job.status, Job),
        total_scopes=await _total(Scope),
        total_targets=await _total(Target),
        total_notes=await _total(Note),
        total_reports=await _total(Report),
    )


@router.patch("/{engagement_id}", response_model=EngagementOut)
async def update_engagement(
    engagement_id: uuid.UUID, payload: EngagementUpdate, db: AsyncSession = Depends(get_db)
) -> Engagement:
    engagement = await _get_engagement_or_404(engagement_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(engagement, field, value)
    await db.commit()
    await db.refresh(engagement)
    return engagement


@router.delete("/{engagement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_engagement(engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    engagement = await _get_engagement_or_404(engagement_id, db)
    await db.delete(engagement)
    await db.commit()
