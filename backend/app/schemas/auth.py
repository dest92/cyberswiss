import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr


class SetupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}


class AuthStatus(BaseModel):
    auth_disabled: bool
    needs_setup: bool
    user: UserOut | None = None
