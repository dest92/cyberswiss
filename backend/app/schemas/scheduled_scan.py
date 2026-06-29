import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class ScheduledScanCreate(BaseModel):
    tool_name: str
    params: dict[str, Any] = {}
    interval_minutes: int


class ScheduledScanUpdate(BaseModel):
    params: dict[str, Any] | None = None
    interval_minutes: int | None = None
    enabled: bool | None = None


class ScheduledScanOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    engagement_id: uuid.UUID
    tool_name: str
    params: dict[str, Any]
    interval_minutes: int
    enabled: bool
    next_run_at: datetime
    last_run_at: datetime | None
    created_at: datetime
