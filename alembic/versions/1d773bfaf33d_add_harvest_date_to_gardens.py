"""Add harvest date to gardens

Revision ID: 1d773bfaf33d
Revises: 8d80e867d3dd
Create Date: 2020-07-24 18:42:46.953457

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '1d773bfaf33d'
down_revision = '8d80e867d3dd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('gardens', sa.Column('harvest_date', sa.DateTime))



def downgrade():
    op.drop_column('gardens', 'harvest_date')
