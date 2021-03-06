"""added chapter and section to exercises

Revision ID: 21bb97866ed8
Revises: 1d806e0d59ad
Create Date: 2016-06-09 14:42:19.130708

"""

# revision identifiers, used by Alembic.
revision = '21bb97866ed8'
down_revision = '1d806e0d59ad'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

subject_table = sa.table('subjects',
                         sa.column('id', sa.Integer),
                         sa.column('name', sa.String),
                         sa.column('tag', sa.String),
                         sa.column('book_url', sa.String))


def upgrade():
    bind = op.get_bind()
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercises', sa.Column('chapter_id', sa.Integer(), nullable=True))
    op.add_column('exercises', sa.Column('section_id', sa.Integer(), nullable=True))
    op.add_column('exercises', sa.Column('book_row_id', sa.Integer(), nullable=True))

    op.add_column('subjects', sa.Column('book_url', sa.String(), nullable=True))
    ### end Alembic commands ###

    data = [
        {'id': 1, 'book_url': 'https://staging-tutor.cnx.org/contents/d52e93f4-8653-4273-86da-3850001c0786'},
        {'id': 2, 'book_url': 'https://staging-tutor.cnx.org/contents/334f8b61-30eb-4475-8e05-5260a4866b4b'}
    ]

    for item in data:
        update = sa.update(subject_table)\
            .where(subject_table.c.id == item['id'])\
            .values(dict(book_url=item['book_url']))
        bind.execute(update)


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('subjects', 'book_url')
    op.drop_column('exercises', 'section_id')
    op.drop_column('exercises', 'chapter_id')
    op.drop_column('exercises', 'book_row_id')
    ### end Alembic commands ###
