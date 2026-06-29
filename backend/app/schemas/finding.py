import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator

from app.knowledge.mitre import MITRE_CODES
from app.knowledge.taxonomy import OWASP_CODES
from app.models.finding import FindingSeverity, FindingStatus


def _validate_owasp_category(value: str) -> str:
    if value not in OWASP_CODES:
        raise ValueError(f"Categoría OWASP inválida: {value}")
    return value


def _validate_mitre_techniques(value: list[str]) -> list[str]:
    invalid = [code for code in value if code not in MITRE_CODES]
    if invalid:
        raise ValueError(f"Técnicas MITRE inválidas: {', '.join(invalid)}")
    return value


class FindingCreate(BaseModel):
    title: str
    description: str | None = None
    owasp_category: str
    mitre_techniques: list[str] = []
    severity: FindingSeverity
    cvss_score: float | None = None
    status: FindingStatus = FindingStatus.open
    source_job_id: uuid.UUID | None = None

    _validate_owasp_category = field_validator("owasp_category")(_validate_owasp_category)
    _validate_mitre_techniques = field_validator("mitre_techniques")(_validate_mitre_techniques)


class FindingUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    owasp_category: str | None = None
    mitre_techniques: list[str] | None = None
    severity: FindingSeverity | None = None
    cvss_score: float | None = None
    status: FindingStatus | None = None

    @field_validator("owasp_category")
    @classmethod
    def validate_owasp_category(cls, value: str | None) -> str | None:
        return _validate_owasp_category(value) if value is not None else value

    @field_validator("mitre_techniques")
    @classmethod
    def validate_mitre_techniques(cls, value: list[str] | None) -> list[str] | None:
        return _validate_mitre_techniques(value) if value is not None else value


class FindingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    engagement_id: uuid.UUID
    source_job_id: uuid.UUID | None
    title: str
    description: str | None
    owasp_category: str
    mitre_techniques: list[str]
    severity: FindingSeverity
    cvss_score: float | None
    status: FindingStatus
    created_at: datetime
    updated_at: datetime
