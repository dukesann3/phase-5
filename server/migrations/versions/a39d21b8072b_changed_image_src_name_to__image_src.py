"""changed image_src name to _image_src

Revision ID: a39d21b8072b
Revises: 8c18ab382a23
Create Date: 2024-04-24 12:25:50.796926

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a39d21b8072b'
down_revision = '8c18ab382a23'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('_image_src', sa.String(), nullable=True))
        batch_op.drop_column('image_src')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_src', sa.VARCHAR(), nullable=True))
        batch_op.drop_column('_image_src')

    # ### end Alembic commands ###
