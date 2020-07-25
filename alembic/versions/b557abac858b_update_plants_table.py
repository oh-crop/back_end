"""Update Plants Table

Revision ID: b557abac858b
Revises: 9575e8399c9f
Create Date: 2020-07-24 18:20:16.487782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b557abac858b'
down_revision = '9575e8399c9f'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column(
    table_name='plants',
    column_name='annual',
    existing_type=sa.Boolean,
    type_=sa.String(50)
    ),
    op.drop_column('plants', 'name')


def downgrade():
    op.alter_column(
    table_name='plants',
    column_name='annual',
    existing_type=sa.String(50),
    type_=sa.Boolean
    ),
    op.add_column('plants', sa.Column('name', sa.String(50)))
