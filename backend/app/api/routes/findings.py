import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.finding import Finding
from app.schemas.finding import FindingCreate, FindingOut, FindingUpdate

router = APIRouter(
    prefix="/api/engagements/{engagement_id}/findings",
    tags=["findings"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[FindingOut])
async def list_findings(
    engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[Finding]:
    result = await db.execute(
        select(Finding)
        .where(Finding.engagement_id == engagement_id)
        .order_by(Finding.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("", response_model=FindingOut, status_code=status.HTTP_201_CREATED)
async def create_finding(
    engagement_id: uuid.UUID, payload: FindingCreate, db: AsyncSession = Depends(get_db)
) -> Finding:
    finding = Finding(engagement_id=engagement_id, **payload.model_dump())
    db.add(finding)
    await db.commit()
    await db.refresh(finding)
    return finding


async def _get_finding_or_404(
    engagement_id: uuid.UUID, finding_id: uuid.UUID, db: AsyncSession
) -> Finding:
    finding = await db.get(Finding, finding_id)
    if finding is None or finding.engagement_id != engagement_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hallazgo no encontrado")
    return finding


@router.patch("/{finding_id}", response_model=FindingOut)
async def update_finding(
    engagement_id: uuid.UUID,
    finding_id: uuid.UUID,
    payload: FindingUpdate,
    db: AsyncSession = Depends(get_db),
) -> Finding:
    finding = await _get_finding_or_404(engagement_id, finding_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(finding, field, value)
    await db.commit()
    await db.refresh(finding)
    return finding


@router.delete("/{finding_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_finding(
    engagement_id: uuid.UUID, finding_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    finding = await _get_finding_or_404(engagement_id, finding_id, db)
    await db.delete(finding)
    await db.commit()
