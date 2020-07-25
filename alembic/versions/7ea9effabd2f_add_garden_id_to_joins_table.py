"""Add garden_id to joins table

Revision ID: 7ea9effabd2f
Revises: 165f21d7f610
Create Date: 2020-07-25 11:49:04.457449

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ea9effabd2f'
down_revision = '165f21d7f610'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('garden_plants', sa.Column('garden_id', sa.Integer, sa.ForeignKey('gardens.id')))


def downgrade():
    op.drop_column('garden_plants', 'garden_id')
