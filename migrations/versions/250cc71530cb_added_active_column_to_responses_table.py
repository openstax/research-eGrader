"""added active column to Responses table

Revision ID: 250cc71530cb
Revises: a052777107f8
Create Date: 2017-02-16 15:15:05.856831

"""

# revision identifiers, used by Alembic.
revision = '250cc71530cb'
down_revision = 'a052777107f8'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('responses', sa.Column('active', sa.Boolean(), nullable=True))
    op.add_column('response_grade', sa.Column('explanation', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('responses', 'active')
    op.drop_column('response_grade', 'explanation')
