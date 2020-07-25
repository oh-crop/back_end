"""Seed garden

Revision ID: 6465b8352ec5
Revises: 7ea9effabd2f
Create Date: 2020-07-25 11:55:15.636226

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column
from sqlalchemy import Integer


# revision identifiers, used by Alembic.
revision = '6465b8352ec5'
down_revision = '7ea9effabd2f'
branch_labels = None
depends_on = None

def upgrade():
    gardens_table = table('gardens',
        column('id', Integer),
    )

    op.bulk_insert(gardens_table,
      [
        {'id':1},
      ]
    )


def downgrade():
    op.execute('''DELETE FROM gardens WHERE id=1; ''')
