"""empty message

Revision ID: fa699be33f95
Revises: 2a553c3a9b4e
Create Date: 2025-01-07 21:11:51.441026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa699be33f95'
down_revision = '2a553c3a9b4e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actives', schema=None) as batch_op:
        batch_op.drop_constraint('fk_actives_user_id_members', type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_actives_user_id_payments'), 'payments', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('actives', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_actives_user_id_payments'), type_='foreignkey')
        batch_op.create_foreign_key('fk_actives_user_id_members', 'members', ['user_id'], ['id'])

    # ### end Alembic commands ###
