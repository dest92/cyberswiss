import uuid
from datetime import datetime

from pydantic import BaseModel

from app.models.report import ReportFormat


class ReportCreate(BaseModel):
    format: ReportFormat


class ReportOut(BaseModel):
    id: uuid.UUID
    engagement_id: uuid.UUID
    format: ReportFormat
    created_at: datetime

    model_config = {"from_attributes": True}
