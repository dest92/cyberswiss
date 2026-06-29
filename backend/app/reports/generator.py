import asyncio
import uuid
from datetime import datetime, timezone
from pathlib import Path

import jinja2
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from weasyprint import HTML

from app.models.engagement import Engagement
from app.models.finding import Finding
from app.models.note import Note
from app.models.scope import Scope

TEMPLATES_DIR = Path(__file__).parent / "templates"

_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(TEMPLATES_DIR)),
    trim_blocks=True,
    lstrip_blocks=True,
)

SEVERITY_ORDER = ["critical", "high", "medium", "low", "info"]


async def _gather_report_context(engagement_id: uuid.UUID, db: AsyncSession) -> dict:
    engagement = await db.get(Engagement, engagement_id)

    scopes = (
        (
            await db.execute(
                select(Scope).where(Scope.engagement_id == engagement_id).order_by(Scope.type)
            )
        )
        .scalars()
        .all()
    )

    findings = (
        (await db.execute(select(Finding).where(Finding.engagement_id == engagement_id)))
        .scalars()
        .all()
    )
    findings_sorted = sorted(findings, key=lambda f: SEVERITY_ORDER.index(f.severity.value))

    notes = (
        (
            await db.execute(
                select(Note).where(Note.engagement_id == engagement_id).order_by(Note.created_at)
            )
        )
        .scalars()
        .all()
    )

    severity_counts = {sev: 0 for sev in SEVERITY_ORDER}
    for finding in findings:
        severity_counts[finding.severity.value] += 1

    return {
        "engagement": engagement,
        "scopes": scopes,
        "findings": findings_sorted,
        "notes": notes,
        "severity_counts": severity_counts,
        "severity_order": SEVERITY_ORDER,
        "generated_at": datetime.now(timezone.utc),
    }


async def render_markdown(engagement_id: uuid.UUID, db: AsyncSession) -> str:
    context = await _gather_report_context(engagement_id, db)
    template = _env.get_template("report.md.jinja2")
    return template.render(**context)


async def render_pdf(engagement_id: uuid.UUID, db: AsyncSession) -> bytes:
    context = await _gather_report_context(engagement_id, db)
    template = _env.get_template("report.html.jinja2")
    html = template.render(**context)
    return await asyncio.to_thread(lambda: HTML(string=html).write_pdf())
