"""added notification types and text is nullable

Revision ID: 54e753846c9c
Revises: 9ab9e7a92a38
Create Date: 2024-04-07 10:02:54.435627

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54e753846c9c'
down_revision = '9ab9e7a92a38'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.alter_column('text',
               existing_type=sa.VARCHAR(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.alter_column('text',
               existing_type=sa.VARCHAR(),
               nullable=False)

    # ### end Alembic commands ###
