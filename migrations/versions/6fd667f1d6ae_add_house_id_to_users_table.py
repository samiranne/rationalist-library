"""Add 'house_id' column to users table, and drop join table house_users

Revision ID: 6fd667f1d6ae
Revises: 88008363f357
Create Date: 2018-05-13 13:32:46.377900

"""

# revision identifiers, used by Alembic.
revision = '6fd667f1d6ae'
down_revision = 'a3e5ffb9c0da'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('house_users')
    op.add_column('users', sa.Column('house_id', sa.Integer(), nullable=False, server_default='1'))
    op.create_foreign_key(None, 'users', 'houses', ['house_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'house_id')
    op.create_table('house_users',
    sa.Column('house_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['house_id'], ['houses.id'], name='house_users_house_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='house_users_user_id_fkey'),
    sa.PrimaryKeyConstraint('house_id', 'user_id', name='house_users_pkey')
    )
    ### end Alembic commands ###
