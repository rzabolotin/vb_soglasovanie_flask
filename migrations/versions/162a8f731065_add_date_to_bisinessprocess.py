"""add date to bisinessprocess

Revision ID: 162a8f731065
Revises: cf4eadd92f65
Create Date: 2020-09-21 14:03:40.276454

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '162a8f731065'
down_revision = 'cf4eadd92f65'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('business_process', sa.Column('date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('business_process', 'date')
    # ### end Alembic commands ###
