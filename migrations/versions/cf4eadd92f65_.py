"""empty message

Revision ID: cf4eadd92f65
Revises: 9bcbfcd99017
Create Date: 2020-09-16 10:42:42.908669

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf4eadd92f65'
down_revision = '9bcbfcd99017'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('full_user_name', sa.String(length=250), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'full_user_name')
    # ### end Alembic commands ###
