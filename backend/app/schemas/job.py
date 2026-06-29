import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict

from app.models.job import JobStatus


class JobCreate(BaseModel):
    tool_name: str
    params: dict[str, Any] = {}


class JobOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    engagement_id: uuid.UUID
    tool_name: str
    status: JobStatus
    params: dict[str, Any]
    raw_output: str | None
    parsed_results: list[dict[str, Any]] | None
    container_id: str | None
    error_message: str | None
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
