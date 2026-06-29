import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.knowledge.taxonomy import OWASP_CODES
from app.models.knowledge_document import KnowledgeDocumentStatus, KnowledgeDocumentType


def _validate_owasp_categories(values: list[str]) -> list[str]:
    for value in values:
        if value not in OWASP_CODES:
            raise ValueError(f"Categoría OWASP inválida: {value}")
    return values


class KnowledgeDocumentCreate(BaseModel):
    title: str
    content: str
    owasp_categories: list[str] = []

    _validate_owasp_categories = field_validator("owasp_categories")(_validate_owasp_categories)


class KnowledgeDocumentUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    owasp_categories: list[str] | None = None

    @field_validator("owasp_categories")
    @classmethod
    def validate_owasp_categories(cls, value: list[str] | None) -> list[str] | None:
        return _validate_owasp_categories(value) if value is not None else value


class KnowledgeDocumentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    doc_type: KnowledgeDocumentType
    status: KnowledgeDocumentStatus
    content: str | None
    file_path: str | None
    owasp_categories: list[str]
    is_seed: bool
    error_message: str | None
    created_at: datetime
    updated_at: datetime


class KnowledgeDocumentSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    doc_type: KnowledgeDocumentType
    status: KnowledgeDocumentStatus
    owasp_categories: list[str]
    is_seed: bool
    created_at: datetime
    updated_at: datetime


class KnowledgeDocumentSearchResult(KnowledgeDocumentSummary):
    snippet: str | None = None
    rank: float | None = None
