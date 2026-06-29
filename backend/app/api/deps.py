from fastapi import Cookie, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User

SESSION_COOKIE_NAME = "cyberswiss_session"


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> User | None:
    if settings.auth_disabled:
        result = await db.execute(select(User).limit(1))
        return result.scalar_one_or_none()

    if session_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")

    user_id = decode_access_token(session_token)
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesión inválida")

    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sesión inválida")

    return user


async def get_current_user_optional(
    db: AsyncSession = Depends(get_db),
    session_token: str | None = Cookie(default=None, alias=SESSION_COOKIE_NAME),
) -> User | None:
    if settings.auth_disabled:
        result = await db.execute(select(User).limit(1))
        return result.scalar_one_or_none()

    if session_token is None:
        return None

    user_id = decode_access_token(session_token)
    if user_id is None:
        return None

    return await db.get(User, user_id)
