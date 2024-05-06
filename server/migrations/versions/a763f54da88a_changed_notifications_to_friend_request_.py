"""changed notifications to friend request notifications

Revision ID: a763f54da88a
Revises: d0058e5fac52
Create Date: 2024-05-06 12:59:32.722309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a763f54da88a'
down_revision = 'd0058e5fac52'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('friend_request_notifications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=False),
    sa.Column('reciever_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['reciever_id'], ['users.id'], name=op.f('fk_friend_request_notifications_reciever_id_users')),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], name=op.f('fk_friend_request_notifications_sender_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_friend_request_notifications')),
    sa.UniqueConstraint('sender_id', 'reciever_id', 'text', name='notification_uniqueness')
    )
    op.drop_table('notifications')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('notifications',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('notification_sender_id', sa.INTEGER(), nullable=False),
    sa.Column('notification_reciever_id', sa.INTEGER(), nullable=False),
    sa.Column('text', sa.VARCHAR(), nullable=False),
    sa.Column('notification_type', sa.VARCHAR(length=14), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('updated_at', sa.DATETIME(), nullable=True),
    sa.ForeignKeyConstraint(['notification_reciever_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['notification_sender_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('notification_sender_id', 'notification_reciever_id', 'text', 'notification_type', name='notification_uniqueness')
    )
    op.drop_table('friend_request_notifications')
    # ### end Alembic commands ###
