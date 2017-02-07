"""add sociology subject to the database

Revision ID: a052777107f8
Revises: cd8b85614a25
Create Date: 2017-02-03 15:35:39.049322

"""

# revision identifiers, used by Alembic.
revision = 'a052777107f8'
down_revision = 'cd8b85614a25'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

subject_table = sa.table('subjects',
                         sa.column('id', sa.Integer),
                         sa.column('name', sa.String),
                         sa.column('tag', sa.String))


def upgrade():
    op.bulk_insert(subject_table,
                   [
                       {'id': 3, 'name': 'Sociology', 'tag': 'book:stax-soc'},
                   ]
                   )


def downgrade():
    pass
