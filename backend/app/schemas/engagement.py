import uuid
from datetime import date, datetime

from pydantic import BaseModel

from app.models.engagement import EngagementStatus


class EngagementCreate(BaseModel):
    name: str
    client_name: str | None = None
    authorization_scope_doc: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class EngagementUpdate(BaseModel):
    name: str | None = None
    client_name: str | None = None
    status: EngagementStatus | None = None
    authorization_scope_doc: str | None = None
    start_date: date | None = None
    end_date: date | None = None


class EngagementSummary(BaseModel):
    findings_by_severity: dict[str, int]
    findings_by_owasp_category: dict[str, int]
    jobs_by_status: dict[str, int]
    total_scopes: int
    total_targets: int
    total_notes: int
    total_reports: int


class EngagementOut(BaseModel):
    id: uuid.UUID
    name: str
    client_name: str | None
    status: EngagementStatus
    authorization_scope_doc: str | None
    start_date: date | None
    end_date: date | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
