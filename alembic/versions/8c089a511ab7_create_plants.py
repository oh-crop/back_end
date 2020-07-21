"""create plants

Revision ID: 8c089a511ab7
Revises:
Create Date: 2020-07-20 17:43:15.553458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c089a511ab7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
    'plants',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String(50)),
        sa.Column('plant_type', sa.String(50)),
        sa.Column('image', sa.Unicode(255)),
        sa.Column('lighting', sa.String(50)),
        sa.Column('water_frequency', sa.Integer),
        sa.Column('harvest_time', sa.Integer, nullable=True),
        sa.Column('root_depth', sa.Integer),
        sa.Column('annual', sa.Boolean),
    )


def downgrade():
    op.drop_table('plants')
