"""merge heads

Revision ID: fd0d1620dcc3
Revises: change_recordatorio_fecha_datetime, merge_heads_20260129
Create Date: 2026-01-31 22:13:36.359656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd0d1620dcc3'
down_revision: Union[str, Sequence[str], None] = ('chg_rec_fecha_dt', 'merge_heads_20260129')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
