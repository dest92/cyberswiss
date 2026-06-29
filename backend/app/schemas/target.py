import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.target import TargetType


class TargetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    engagement_id: uuid.UUID
    type: TargetType
    value: str
    source_job_id: uuid.UUID | None
    discovered_at: datetime
