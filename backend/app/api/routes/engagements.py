import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.engagement import Engagement
from app.schemas.engagement import EngagementCreate, EngagementOut, EngagementUpdate

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
