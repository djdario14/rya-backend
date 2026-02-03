"""
Alembic migration script to change 'fecha' and 'creado_en' columns in 'recordatorios' table from Date to DateTime.
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'chg_rec_fecha_dt'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.alter_column('recordatorios', 'fecha',
               existing_type=sa.Date(),
               type_=sa.DateTime(),
               existing_nullable=False)
    op.alter_column('recordatorios', 'creado_en',
               existing_type=sa.Date(),
               type_=sa.DateTime(),
               existing_nullable=False)

def downgrade():
    op.alter_column('recordatorios', 'fecha',
               existing_type=sa.DateTime(),
               type_=sa.Date(),
               existing_nullable=False)
    op.alter_column('recordatorios', 'creado_en',
               existing_type=sa.DateTime(),
               type_=sa.Date(),
               existing_nullable=False)
