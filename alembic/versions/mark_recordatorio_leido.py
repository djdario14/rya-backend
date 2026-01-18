"""
Revision ID: mark_recordatorio_leido
Revises: 
Create Date: 2026-01-17
"""

revision = 'mark_recordatorio_leido'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('recordatorios', sa.Column('leido', sa.Integer(), nullable=False, server_default='0'))

def downgrade():
    op.drop_column('recordatorios', 'leido')
