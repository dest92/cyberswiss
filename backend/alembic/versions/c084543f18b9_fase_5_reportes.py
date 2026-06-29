"""fase 5 reportes

Revision ID: c084543f18b9
Revises: f449f824bb08
Create Date: 2026-06-29 08:41:26.235342

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = 'c084543f18b9'
down_revision: str | None = 'f449f824bb08'
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('reports',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('engagement_id', sa.UUID(), nullable=False),
    sa.Column('format', sa.Enum('markdown', 'pdf', name='report_format'), nullable=False),
    sa.Column('file_path', sa.String(length=512), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['engagement_id'], ['engagements.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('reports')
