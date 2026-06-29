"""fase 6 mitre techniques en findings

Revision ID: 48604da8969b
Revises: 9b1a39cffecb
Create Date: 2026-06-29 09:11:49.595603

"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '48604da8969b'
down_revision: str | None = '9b1a39cffecb'
branch_labels: Sequence[str] | None = None
depends_on: Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        'findings',
        sa.Column(
            'mitre_techniques',
            postgresql.ARRAY(sa.String(length=16)),
            nullable=False,
            server_default='{}',
        ),
    )


def downgrade() -> None:
    op.drop_column('findings', 'mitre_techniques')
