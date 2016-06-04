"""added firstname lastname subject fields to registration form

Revision ID: 4c9077858c3c
Revises: a7fae591baaf
Create Date: 2016-06-03 23:20:37.680700

"""

# revision identifiers, used by Alembic.
revision = '4c9077858c3c'
down_revision = 'a7fae591baaf'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_profile')
    op.add_column('users', sa.Column('first_name', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('last_name', sa.String(length=100), nullable=True))
    op.add_column('users', sa.Column('subject_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'subjects', ['subject_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'subject_id')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'first_name')
    op.create_table('user_profile',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('first_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.Column('last_name', sa.VARCHAR(length=100), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name=u'user_profile_pkey')
    )
    ### end Alembic commands ###
