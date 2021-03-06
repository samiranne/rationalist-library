"""Rename house_member to house_membership; rename member_id to user_id

Revision ID: dd06b715ef7c
Revises: ed1f0de54044
Create Date: 2018-10-26 14:24:07.428397

"""

# revision identifiers, used by Alembic.
revision = 'dd06b715ef7c'
down_revision = 'ed1f0de54044'

from alembic import op
import sqlalchemy as sa


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('house_memberships',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('house_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['house_id'], ['houses.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('house_members')
    op.add_column('house_membership_requests', sa.Column('user_id', sa.Integer(), nullable=False))
    op.drop_constraint('house_membership_requests_member_id_fkey', 'house_membership_requests', type_='foreignkey')
    op.create_foreign_key(None, 'house_membership_requests', 'users', ['user_id'], ['id'])
    op.drop_column('house_membership_requests', 'member_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('house_membership_requests', sa.Column('member_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'house_membership_requests', type_='foreignkey')
    op.create_foreign_key('house_membership_requests_member_id_fkey', 'house_membership_requests', 'users', ['member_id'], ['id'])
    op.drop_column('house_membership_requests', 'user_id')
    op.create_table('house_members',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('house_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('member_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('is_admin', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['house_id'], ['houses.id'], name='house_members_house_id_fkey'),
    sa.ForeignKeyConstraint(['member_id'], ['users.id'], name='house_members_member_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='house_members_pkey')
    )
    op.drop_table('house_memberships')
    # ### end Alembic commands ###
