import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.report import Report, ReportFormat
from app.reports.generator import render_markdown, render_pdf
from app.schemas.report import ReportCreate, ReportOut

router = APIRouter(
    prefix="/api/engagements/{engagement_id}/reports",
    tags=["reports"],
    dependencies=[Depends(get_current_user)],
)

MEDIA_TYPES = {
    ReportFormat.markdown: "text/markdown",
    ReportFormat.pdf: "application/pdf",
}
EXTENSIONS = {
    ReportFormat.markdown: "md",
    ReportFormat.pdf: "pdf",
}


@router.get("", response_model=list[ReportOut])
async def list_reports(engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> list[Report]:
    result = await db.execute(
        select(Report).where(Report.engagement_id == engagement_id).order_by(Report.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("", response_model=ReportOut, status_code=status.HTTP_201_CREATED)
async def create_report(
    engagement_id: uuid.UUID, payload: ReportCreate, db: AsyncSession = Depends(get_db)
) -> Report:
    reports_dir = Path(settings.reports_dir)
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_id = uuid.uuid4()
    file_path = reports_dir / f"{report_id}.{EXTENSIONS[payload.format]}"

    if payload.format == ReportFormat.markdown:
        content = await render_markdown(engagement_id, db)
        file_path.write_text(content)
    else:
        pdf_bytes = await render_pdf(engagement_id, db)
        file_path.write_bytes(pdf_bytes)

    report = Report(
        id=report_id, engagement_id=engagement_id, format=payload.format, file_path=str(file_path)
    )
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


async def _get_report_or_404(engagement_id: uuid.UUID, report_id: uuid.UUID, db: AsyncSession) -> Report:
    report = await db.get(Report, report_id)
    if report is None or report.engagement_id != engagement_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reporte no encontrado")
    return report


@router.get("/{report_id}/download")
async def download_report(
    engagement_id: uuid.UUID, report_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> FileResponse:
    report = await _get_report_or_404(engagement_id, report_id, db)
    filename = f"reporte-{engagement_id}.{EXTENSIONS[report.format]}"
    return FileResponse(report.file_path, media_type=MEDIA_TYPES[report.format], filename=filename)


@router.delete("/{report_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_report(
    engagement_id: uuid.UUID, report_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    report = await _get_report_or_404(engagement_id, report_id, db)
    Path(report.file_path).unlink(missing_ok=True)
    await db.delete(report)
    await db.commit()
