import asyncio
import uuid

import dramatiq
import pdfplumber

from app.db.session import SessionLocal
from app.models.knowledge_document import KnowledgeDocument, KnowledgeDocumentStatus
from app.workers.broker import redis_broker  # noqa: F401  (configures the dramatiq broker)


def _extract_pdf_text(file_path: str) -> str:
    pages = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            pages.append(page.extract_text() or "")
    return "\n\n".join(pages).strip()


async def _process_knowledge_document_async(document_id: str) -> None:
    async with SessionLocal() as db:
        document = await db.get(KnowledgeDocument, uuid.UUID(document_id))
        if document is None:
            return

        try:
            text = await asyncio.to_thread(_extract_pdf_text, document.file_path)
        except Exception as exc:
            document.status = KnowledgeDocumentStatus.failed
            document.error_message = str(exc)
        else:
            document.content = text
            document.status = KnowledgeDocumentStatus.ready

        await db.commit()


@dramatiq.actor(max_retries=0, time_limit=120_000)
def process_knowledge_document(document_id: str) -> None:
    asyncio.run(_process_knowledge_document_async(document_id))
