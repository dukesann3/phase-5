"""notification update

Revision ID: e748ae20603d
Revises: c46ac3dd1941
Create Date: 2024-04-07 13:51:51.751613

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e748ae20603d'
down_revision = 'c46ac3dd1941'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notification_type', sa.Enum('Friend Request', 'Comment', 'Message', 'Like', name='notification_type'), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notifications', schema=None) as batch_op:
        batch_op.drop_column('notification_type')

    # ### end Alembic commands ###
