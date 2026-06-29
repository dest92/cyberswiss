from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import SESSION_COOKIE_NAME, get_current_user, get_current_user_optional
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import AuthStatus, LoginRequest, SetupRequest, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])

COOKIE_MAX_AGE = settings.jwt_expire_minutes * 60


def _set_session_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        max_age=COOKIE_MAX_AGE,
    )


@router.get("/status", response_model=AuthStatus)
async def auth_status(
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_current_user_optional),
) -> AuthStatus:
    result = await db.execute(select(User).limit(1))
    any_user = result.scalar_one_or_none()
    return AuthStatus(
        auth_disabled=settings.auth_disabled,
        needs_setup=any_user is None,
        user=UserOut.model_validate(current_user) if current_user else None,
    )


@router.post("/setup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def setup(payload: SetupRequest, response: Response, db: AsyncSession = Depends(get_db)) -> User:
    existing = await db.execute(select(User).limit(1))
    if existing.scalar_one_or_none() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ya existe un usuario configurado")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_access_token(user.id)
    _set_session_cookie(response, token)
    return user


@router.post("/login", response_model=UserOut)
async def login(payload: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)) -> User:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user is None or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    token = create_access_token(user.id)
    _set_session_cookie(response, token)
    return user


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response) -> None:
    response.delete_cookie(SESSION_COOKIE_NAME)


@router.get("/me", response_model=UserOut)
async def me(current_user: User | None = Depends(get_current_user)) -> User:
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No autenticado")
    return current_user
