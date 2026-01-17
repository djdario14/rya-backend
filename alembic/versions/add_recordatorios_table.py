"""
add recordatorios table
"""
revision = 'add_recordatorios_table'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'recordatorios',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('cliente_id', sa.Integer, sa.ForeignKey('clientes.id'), nullable=False),
        sa.Column('fecha', sa.DateTime, nullable=False),
        sa.Column('nota', sa.String, nullable=True),
        sa.Column('creado_en', sa.DateTime, nullable=False),
    )

def downgrade():
    op.drop_table('recordatorios')
