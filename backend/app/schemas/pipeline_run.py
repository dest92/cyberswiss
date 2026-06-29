import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.pipeline_run import PipelineRunStatus
from app.schemas.job import JobOut


class PipelineRunCreate(BaseModel):
    pipeline_name: str
    params: dict[str, Any] = {}


class PipelineRunOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    engagement_id: uuid.UUID
    pipeline_name: str
    status: PipelineRunStatus
    params: dict[str, Any]
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    jobs: list[JobOut] = []
