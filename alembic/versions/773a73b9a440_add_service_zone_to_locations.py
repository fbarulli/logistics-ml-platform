"""add service zone to locations

Revision ID: 773a73b9a440
Revises: 0a9a29d08f7f
Create Date: 2026-07-15 11:31:32.172062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '773a73b9a440'
down_revision: Union[str, Sequence[str], None] = '0a9a29d08f7f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "locations",
        sa.Column("service_zone", sa.String(), nullable=True)
    )


def downgrade() -> None:
    op.drop_column(
        "locations",
        "service_zone"
    )
