"""empty message

Revision ID: 6764a0af7c0d
Revises: 24adf5838fd3
Create Date: 2025-01-23 15:16:16.445724

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6764a0af7c0d'
down_revision = '24adf5838fd3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.add_column(sa.Column('type', sa.String(length=16), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tokens', schema=None) as batch_op:
        batch_op.drop_column('type')

    # ### end Alembic commands ###
