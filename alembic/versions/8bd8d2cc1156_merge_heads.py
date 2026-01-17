"""merge heads

Revision ID: 8bd8d2cc1156
Revises: add_motivo_no_pago_to_pagos, add_recordatorios_table
Create Date: 2026-01-17 17:51:02.573952

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8bd8d2cc1156'
down_revision: Union[str, Sequence[str], None] = ('add_motivo_no_pago_to_pagos', 'add_recordatorios_table')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
