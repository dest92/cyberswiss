import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.scope import Scope
from app.schemas.scope import ScopeCreate, ScopeOut, ScopeUpdate

router = APIRouter(
    prefix="/api/engagements/{engagement_id}/scopes",
    tags=["scopes"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[ScopeOut])
async def list_scopes(engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> list[Scope]:
    result = await db.execute(select(Scope).where(Scope.engagement_id == engagement_id))
    return list(result.scalars().all())


@router.post("", response_model=ScopeOut, status_code=status.HTTP_201_CREATED)
async def create_scope(
    engagement_id: uuid.UUID, payload: ScopeCreate, db: AsyncSession = Depends(get_db)
) -> Scope:
    scope = Scope(engagement_id=engagement_id, **payload.model_dump())
    db.add(scope)
    await db.commit()
    await db.refresh(scope)
    return scope


async def _get_scope_or_404(engagement_id: uuid.UUID, scope_id: uuid.UUID, db: AsyncSession) -> Scope:
    scope = await db.get(Scope, scope_id)
    if scope is None or scope.engagement_id != engagement_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Scope no encontrado")
    return scope


@router.patch("/{scope_id}", response_model=ScopeOut)
async def update_scope(
    engagement_id: uuid.UUID,
    scope_id: uuid.UUID,
    payload: ScopeUpdate,
    db: AsyncSession = Depends(get_db),
) -> Scope:
    scope = await _get_scope_or_404(engagement_id, scope_id, db)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(scope, field, value)
    await db.commit()
    await db.refresh(scope)
    return scope


@router.delete("/{scope_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scope(
    engagement_id: uuid.UUID, scope_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    scope = await _get_scope_or_404(engagement_id, scope_id, db)
    await db.delete(scope)
    await db.commit()
