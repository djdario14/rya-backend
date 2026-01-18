"""
Revision ID: mark_recordatorio_leido
Revises: 
Create Date: 2026-01-17
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('recordatorios', sa.Column('leido', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('recordatorios', 'leido')
