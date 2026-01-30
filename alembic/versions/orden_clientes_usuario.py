"""
Revision ID: orden_clientes_usuario
Revises: 
Create Date: 2026-01-29
"""

# revision identifiers, used by Alembic.
revision = 'orden_clientes_usuario'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'orden_clientes_usuario',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('usuario_id', sa.Integer, sa.ForeignKey('usuarios.id'), nullable=False),
        sa.Column('orden', sa.JSON, nullable=False)
    )

def downgrade():
    op.drop_table('orden_clientes_usuario')
