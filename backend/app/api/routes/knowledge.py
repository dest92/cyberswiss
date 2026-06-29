import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.core.config import settings
from app.db.session import get_db
from app.models.knowledge_document import (
    KnowledgeDocument,
    KnowledgeDocumentStatus,
    KnowledgeDocumentType,
)
from app.schemas.knowledge_document import (
    KnowledgeDocumentCreate,
    KnowledgeDocumentOut,
    KnowledgeDocumentSearchResult,
    KnowledgeDocumentSummary,
    KnowledgeDocumentUpdate,
)
from app.workers.knowledge_actors import process_knowledge_document

router = APIRouter(
    prefix="/api/knowledge",
    tags=["knowledge"],
    dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=list[KnowledgeDocumentSummary])
async def list_documents(
    owasp_category: str | None = None, db: AsyncSession = Depends(get_db)
) -> list[KnowledgeDocument]:
    query = select(KnowledgeDocument).order_by(KnowledgeDocument.title)
    if owasp_category:
        query = query.where(
            text("owasp_categories ? :category").bindparams(category=owasp_category)
        )
    result = await db.execute(query)
    return list(result.scalars().all())


@router.get("/search", response_model=list[KnowledgeDocumentSearchResult])
async def search_documents(q: str, db: AsyncSession = Depends(get_db)) -> list[dict]:
    result = await db.execute(
        text(
            """
            SELECT id, title, doc_type, status, owasp_categories, is_seed,
                   created_at, updated_at,
                   ts_headline('spanish', coalesce(content, ''), plainto_tsquery('spanish', :q),
                               'MaxFragments=1, MaxWords=40, MinWords=15') AS snippet,
                   ts_rank(search_vector, plainto_tsquery('spanish', :q)) AS rank
            FROM knowledge_documents
            WHERE search_vector @@ plainto_tsquery('spanish', :q)
            ORDER BY rank DESC
            LIMIT 50
            """
        ),
        {"q": q},
    )
    return [dict(row._mapping) for row in result]


@router.get("/{document_id}", response_model=KnowledgeDocumentOut)
async def get_document(
    document_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> KnowledgeDocument:
    document = await db.get(KnowledgeDocument, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")
    return document


@router.post("", response_model=KnowledgeDocumentOut, status_code=status.HTTP_201_CREATED)
async def create_document(
    payload: KnowledgeDocumentCreate, db: AsyncSession = Depends(get_db)
) -> KnowledgeDocument:
    document = KnowledgeDocument(
        title=payload.title,
        content=payload.content,
        doc_type=KnowledgeDocumentType.markdown,
        status=KnowledgeDocumentStatus.ready,
        owasp_categories=payload.owasp_categories,
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)
    return document


@router.post(
    "/upload", response_model=KnowledgeDocumentOut, status_code=status.HTTP_201_CREATED
)
async def upload_document(
    title: str = Form(...),
    owasp_categories: str = Form(""),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
) -> KnowledgeDocument:
    categories = [c.strip() for c in owasp_categories.split(",") if c.strip()]

    uploads_dir = Path(settings.uploads_dir)
    uploads_dir.mkdir(parents=True, exist_ok=True)
    file_path = uploads_dir / f"{uuid.uuid4()}.pdf"
    file_path.write_bytes(await file.read())

    document = KnowledgeDocument(
        title=title,
        doc_type=KnowledgeDocumentType.pdf,
        status=KnowledgeDocumentStatus.processing,
        file_path=str(file_path),
        owasp_categories=categories,
    )
    db.add(document)
    await db.commit()
    await db.refresh(document)

    process_knowledge_document.send(str(document.id))
    return document


@router.patch("/{document_id}", response_model=KnowledgeDocumentOut)
async def update_document(
    document_id: uuid.UUID, payload: KnowledgeDocumentUpdate, db: AsyncSession = Depends(get_db)
) -> KnowledgeDocument:
    document = await db.get(KnowledgeDocument, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(document, field, value)
    await db.commit()
    await db.refresh(document)
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    document = await db.get(KnowledgeDocument, document_id)
    if document is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Documento no encontrado")
    if document.file_path:
        Path(document.file_path).unlink(missing_ok=True)
    await db.delete(document)
    await db.commit()
