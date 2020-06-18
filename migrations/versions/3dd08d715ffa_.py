"""empty message

Revision ID: 3dd08d715ffa
Revises: 
Create Date: 2020-05-06 15:58:22.207996

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3dd08d715ffa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('invited_user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('invite_code', sa.String(length=64), nullable=False),
    sa.Column('role', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('roles')
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'role')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('role', sa.INTEGER(), nullable=True))
    op.create_foreign_key(None, 'users', 'roles', ['role'], ['id'])
    op.create_table('roles',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=64), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('invited_user')
    # ### end Alembic commands ###