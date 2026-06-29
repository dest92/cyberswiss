import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class FindingSeverity(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"


class FindingStatus(str, enum.Enum):
    open = "open"
    confirmed = "confirmed"
    fixed = "fixed"
    false_positive = "false_positive"


class Finding(Base):
    __tablename__ = "findings"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE"), nullable=False
    )
    source_job_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    owasp_category: Mapped[str] = mapped_column(String(16), nullable=False)
    severity: Mapped[FindingSeverity] = mapped_column(
        SqlEnum(FindingSeverity, name="finding_severity"), nullable=False
    )
    cvss_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    status: Mapped[FindingStatus] = mapped_column(
        SqlEnum(FindingStatus, name="finding_status"), default=FindingStatus.open, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False
    )

    engagement = relationship("Engagement", back_populates="findings")
