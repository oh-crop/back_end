"""Rename Garden Table

Revision ID: 45d3bf115dcd
Revises: 1d773bfaf33d
Create Date: 2020-07-25 11:42:41.264952

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45d3bf115dcd'
down_revision = '1d773bfaf33d'
branch_labels = None
depends_on = None


def upgrade():
    op.rename_table('gardens', 'garden_plants')


def downgrade():
    op.rename_table('garden_plants', 'gardens')
