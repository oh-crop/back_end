"""Create New Garden Table

Revision ID: 165f21d7f610
Revises: 45d3bf115dcd
Create Date: 2020-07-25 11:46:58.286637

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '165f21d7f610'
down_revision = '45d3bf115dcd'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'gardens',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    )


def downgrade():
    op.drop_table('gardens')
