import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteOut, NoteUpdate

router = APIRouter(
    prefix="/api/engagements/{engagement_id}/notes",
    tags=["notes"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[NoteOut])
async def list_notes(engagement_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> list[Note]:
    result = await db.execute(
        select(Note).where(Note.engagement_id == engagement_id).order_by(Note.created_at.desc())
    )
    return list(result.scalars().all())


@router.post("", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
async def create_note(
    engagement_id: uuid.UUID, payload: NoteCreate, db: AsyncSession = Depends(get_db)
) -> Note:
    note = Note(engagement_id=engagement_id, **payload.model_dump())
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def _get_note_or_404(engagement_id: uuid.UUID, note_id: uuid.UUID, db: AsyncSession) -> Note:
    note = await db.get(Note, note_id)
    if note is None or note.engagement_id != engagement_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nota no encontrada")
    return note


@router.patch("/{note_id}", response_model=NoteOut)
async def update_note(
    engagement_id: uuid.UUID,
    note_id: uuid.UUID,
    payload: NoteUpdate,
    db: AsyncSession = Depends(get_db),
) -> Note:
    note = await _get_note_or_404(engagement_id, note_id, db)
    note.content = payload.content
    await db.commit()
    await db.refresh(note)
    return note


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    engagement_id: uuid.UUID, note_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> None:
    note = await _get_note_or_404(engagement_id, note_id, db)
    await db.delete(note)
    await db.commit()
