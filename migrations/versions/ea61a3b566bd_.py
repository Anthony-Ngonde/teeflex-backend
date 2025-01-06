"""empty message

Revision ID: ea61a3b566bd
Revises: b56a53f20ae6
Create Date: 2025-01-06 17:09:57.984483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea61a3b566bd'
down_revision = 'b56a53f20ae6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=15),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.alter_column('phone_number',
               existing_type=sa.String(length=15),
               type_=sa.VARCHAR(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###
