"""added response_grade constraint

Revision ID: 00032b55963b
Revises: 8416c2233a9e
Create Date: 2016-09-14 13:24:21.776314

"""

# revision identifiers, used by Alembic.
revision = '00032b55963b'
down_revision = '8416c2233a9e'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_index('user_id_response_id_unique', 'response_grade', ['response_id', 'user_id'], unique=True)


def downgrade():
    op.drop_index('user_id_response_id_unique')
