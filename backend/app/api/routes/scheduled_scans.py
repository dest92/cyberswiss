import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.scheduled_scan import ScheduledScan
from app.schemas.scheduled_scan import ScheduledScanCreate, ScheduledScanOut, ScheduledScanUpdate
from app.tools import registry

router = APIRouter(
    prefix="/api/engagements/{engagement_id}/scheduled-scans",
    tags=["scheduled-scans"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[ScheduledScanOut])
async def list_scheduled_scans(
    engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> list[ScheduledScan]:
    result = await db.execute(
        select(ScheduledScan)
        .where(ScheduledScan.engagement_id == engagement_id)
        .order_by(ScheduledScan.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("", response_model=ScheduledScanOut, status_code=status.HTTP_201_CREATED)
async def create_scheduled_scan(
    engagement_id: uuid.UUID, payload: ScheduledScanCreate, db: AsyncSession = Depends(get_db)
) -> ScheduledScan:
    if payload.tool_name not in registry.list_tools():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Herramienta desconocida: {payload.tool_name}",
        )
    if payload.interval_minutes < 5:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El intervalo mínimo es de 5 minutos",
        )

    scheduled_scan = ScheduledScan(
        engagement_id=engagement_id,
        tool_name=payload.tool_name,
        params=payload.params,
        interval_minutes=payload.interval_minutes,
        next_run_at=datetime.now(timezone.utc) + timedelta(minutes=payload.interval_minutes),
    )
    db.add(scheduled_scan)
    await db.commit()
    await db.refresh(scheduled_scan)
    return scheduled_scan


async def _get_scheduled_scan_or_404(
    engagement_id: uuid.UUID, scheduled_scan_id: uuid.UUID, db: AsyncSession
) -> ScheduledScan:
    scheduled_scan = await db.get(ScheduledScan, scheduled_scan_id)
    if scheduled_scan is None or scheduled_scan.engagement_id != engagement_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Escaneo recurrente no encontrado"
        )
    return scheduled_scan


@router.patch("/{scheduled_scan_id}", response_model=ScheduledScanOut)
async def update_scheduled_scan(
    engagement_id: uuid.UUID,
    scheduled_scan_id: uuid.UUID,
    payload: ScheduledScanUpdate,
    db: AsyncSession = Depends(get_db),
) -> ScheduledScan:
    scheduled_scan = await _get_scheduled_scan_or_404(engagement_id, scheduled_scan_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(scheduled_scan, field, value)
    await db.commit()
    await db.refresh(scheduled_scan)
    return scheduled_scan


@router.delete("/{scheduled_scan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scheduled_scan(
    engagement_id: uuid.UUID, scheduled_scan_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    scheduled_scan = await _get_scheduled_scan_or_404(engagement_id, scheduled_scan_id, db)
    await db.delete(scheduled_scan)
    await db.commit()
