"""empty message

Revision ID: 9d8bc27d5d2f
Revises: eb4446cfc3ca
Create Date: 2025-01-06 18:12:40.891718

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d8bc27d5d2f'
down_revision = 'eb4446cfc3ca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('member_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_payments_member_id_members'), 'members', ['member_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('payments', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_payments_member_id_members'), type_='foreignkey')
        batch_op.drop_column('member_id')

    # ### end Alembic commands ###
