"""empty message

Revision ID: 8c53463573c6
Revises: 0626004a804e
Create Date: 2021-08-13 07:56:56.137675

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8c53463573c6'
down_revision = '0626004a804e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('shows', sa.Column('id', sa.Integer(), nullable=False))
    op.alter_column('shows', 'start_time',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('shows', 'start_time',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('shows', 'id')
    # ### end Alembic commands ###
