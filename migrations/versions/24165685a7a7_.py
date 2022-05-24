"""empty message

Revision ID: 24165685a7a7
Revises: 
Create Date: 2022-05-21 13:10:14.278008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '24165685a7a7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('firstName', sa.String(length=50), nullable=True),
    sa.Column('lastName', sa.String(length=50), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=300), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=True),
    sa.Column('token', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('followers',
    sa.Column('followerID', sa.String(length=32), nullable=True),
    sa.Column('followedID', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['followedID'], ['user.id'], ),
    sa.ForeignKeyConstraint(['followerID'], ['user.id'], )
    )
    op.create_table('pokemon',
    sa.Column('id', sa.String(length=32), nullable=False),
    sa.Column('name', sa.Text(), nullable=True),
    sa.Column('height', sa.Text(), nullable=True),
    sa.Column('weight', sa.Text(), nullable=True),
    sa.Column('type1', sa.Text(), nullable=True),
    sa.Column('type2', sa.Text(), nullable=True),
    sa.Column('dateCreated', sa.DateTime(), nullable=True),
    sa.Column('author', sa.String(length=32), nullable=True),
    sa.ForeignKeyConstraint(['author'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pokemon')
    op.drop_table('followers')
    op.drop_table('user')
    # ### end Alembic commands ###