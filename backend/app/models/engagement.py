import enum
import uuid
from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class EngagementStatus(str, enum.Enum):
    active = "active"
    archived = "archived"
    closed = "closed"


class Engagement(Base):
    """Raíz de un proyecto de pentest: nombre, cliente, alcance autorizado y fechas."""

    __tablename__ = "engagements"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255))
    client_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[EngagementStatus] = mapped_column(
        Enum(EngagementStatus, name="engagement_status"), default=EngagementStatus.active
    )
    authorization_scope_doc: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    scopes: Mapped[list["Scope"]] = relationship(
        back_populates="engagement", cascade="all, delete-orphan"
    )
    notes: Mapped[list["Note"]] = relationship(
        back_populates="engagement", cascade="all, delete-orphan"
    )
    jobs: Mapped[list["Job"]] = relationship(
        back_populates="engagement", cascade="all, delete-orphan"
    )
    targets: Mapped[list["Target"]] = relationship(
        back_populates="engagement", cascade="all, delete-orphan"
    )
    pipeline_runs: Mapped[list["PipelineRun"]] = relationship(
        back_populates="engagement", cascade="all, delete-orphan"
    )
    findings: Mapped[list["Finding"]] = relationship(
        back_populates="engagement", cascade="all, delete-orphan"
    )
