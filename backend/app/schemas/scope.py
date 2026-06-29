import uuid

from pydantic import BaseModel

from app.models.scope import ScopeType


class ScopeCreate(BaseModel):
    type: ScopeType
    value: str
    in_scope: bool = True


class ScopeUpdate(BaseModel):
    type: ScopeType | None = None
    value: str | None = None
    in_scope: bool | None = None


class ScopeOut(BaseModel):
    id: uuid.UUID
    engagement_id: uuid.UUID
    type: ScopeType
    value: str
    in_scope: bool

    model_config = {"from_attributes": True}
