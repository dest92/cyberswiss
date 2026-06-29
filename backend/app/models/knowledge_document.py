import enum
import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class KnowledgeDocumentType(str, enum.Enum):
    markdown = "markdown"
    pdf = "pdf"


class KnowledgeDocumentStatus(str, enum.Enum):
    ready = "ready"
    processing = "processing"
    failed = "failed"


class KnowledgeDocument(Base):
    """Documento de la biblioteca de conocimiento: cheatsheet en markdown o PDF
    subido por el usuario, clasificado por categoría(s) OWASP Top 10."""

    __tablename__ = "knowledge_documents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    doc_type: Mapped[KnowledgeDocumentType] = mapped_column(
        SqlEnum(KnowledgeDocumentType, name="knowledge_document_type"), nullable=False
    )
    status: Mapped[KnowledgeDocumentStatus] = mapped_column(
        SqlEnum(KnowledgeDocumentStatus, name="knowledge_document_status"),
        default=KnowledgeDocumentStatus.ready,
        nullable=False,
    )
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    file_path: Mapped[str | None] = mapped_column(String(512), nullable=True)
    owasp_categories: Mapped[list] = mapped_column(JSONB, default=list, nullable=False)
    is_seed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )
