"""
Revision ID: add_ubicacion_to_clientes
Revises: 
Create Date: 2026-01-18
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_ubicacion_to_clientes'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('clientes', sa.Column('ubicacion', sa.String(), nullable=True))

def downgrade():
    op.drop_column('clientes', 'ubicacion')
