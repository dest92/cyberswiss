"""fase 6 escaneos recurrentes

Revision ID: 9b1a39cffecb
Revises: c084543f18b9
Create Date: 2026-06-29 08:55:40.025761

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '9b1a39cffecb'
down_revision: str | None = 'c084543f18b9'
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.create_table('scheduled_scans',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('engagement_id', sa.UUID(), nullable=False),
    sa.Column('tool_name', sa.String(length=64), nullable=False),
    sa.Column('params', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    sa.Column('interval_minutes', sa.Integer(), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('next_run_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('last_run_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['engagement_id'], ['engagements.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('scheduled_scans')
