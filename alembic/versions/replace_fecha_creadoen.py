"""
Revision ID: replace_fecha_creadoen
Revises: 
Create Date: 2026-01-28
"""
# Esta migración no realiza cambios porque la columna 'creado_en' ya existe y 'fecha' ya no existe.
from alembic import op
import sqlalchemy as sa

revision = 'replace_fecha_creadoen'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    pass

def downgrade():
    pass
