"""
Migration script to add gastos table
"""
# Alembic identifiers
revision = 'add_gastos_table'
down_revision = None
branch_labels = None
depends_on = None
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        'gastos',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('monto', sa.Float, nullable=False),
        sa.Column('descripcion', sa.String, nullable=False),
        sa.Column('fecha', sa.Date, nullable=False),
    )

def downgrade():
    op.drop_table('gastos')
