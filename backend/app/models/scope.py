import enum
import uuid

from sqlalchemy import Boolean, Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ScopeType(str, enum.Enum):
    domain = "domain"
    ip_range = "ip_range"
    url = "url"
    cidr = "cidr"


class Scope(Base):
    """Target autorizado (o explícitamente excluido) dentro de un Engagement."""

    __tablename__ = "scopes"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    engagement_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("engagements.id", ondelete="CASCADE")
    )
    type: Mapped[ScopeType] = mapped_column(Enum(ScopeType, name="scope_type"))
    value: Mapped[str] = mapped_column(String(255))
    in_scope: Mapped[bool] = mapped_column(Boolean, default=True)

    engagement: Mapped["Engagement"] = relationship(back_populates="scopes")  # noqa: F821
