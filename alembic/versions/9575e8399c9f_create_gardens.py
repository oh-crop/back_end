"""create gardens

Revision ID: 9575e8399c9f
Revises: 752c338c6328
Create Date: 2020-07-23 20:37:51.139055

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '9575e8399c9f'
down_revision = '752c338c6328'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
    'gardens',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('plant_id', sa.Integer, sa.ForeignKey('plants.id')),
        sa.Column('plant_name', sa.String(60)),
        sa.Column('last_watered', sa.DateTime),
        sa.Column('date_added', sa.DateTime, default=datetime.now()),
    )


def downgrade():
    op.drop_table('gardens')
