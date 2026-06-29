import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.target import Target
from app.schemas.target import TargetOut

router = APIRouter(
    prefix="/api/engagements/{engagement_id}/targets",
    tags=["targets"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[TargetOut])
async def list_targets(
    engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[Target]:
    result = await db.execute(
        select(Target)
        .where(Target.engagement_id == engagement_id)
        .order_by(Target.discovered_at.desc())
    )
    return list(result.scalars().all())
