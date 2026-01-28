"""
Revision ID: add_fecha_to_cliente
Revises: None
Create Date: 2026-01-27
"""

revision = 'add_fecha_to_cliente'
down_revision = 'add_motivo_no_pago_to_pagos'
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa
from datetime import date

def upgrade():
    op.add_column('clientes', sa.Column('fecha', sa.Date(), nullable=False, server_default=sa.text(f"'{date.today()}'")))
    op.alter_column('clientes', 'fecha', server_default=None)

def downgrade():
    op.drop_column('clientes', 'fecha')
