"""
Migration script to add motivo_no_pago column to pagos table
"""
from alembic import op
import sqlalchemy as sa

# Alembic identifiers
revision = 'add_motivo_no_pago_to_pagos'
down_revision = 'add_gastos_table'
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('pagos', sa.Column('motivo_no_pago', sa.String, nullable=True))

def downgrade():
    op.drop_column('pagos', 'motivo_no_pago')
