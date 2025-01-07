"""Active column

Revision ID: dfcd30f32a4b
Revises: 2b2562e53a68
Create Date: 2025-01-07 07:44:21.371056

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfcd30f32a4b'
down_revision = '2b2562e53a68'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actives',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.Boolean(), nullable=False),
    sa.Column('date_paid', sa.DateTime(), nullable=False),
    sa.Column('expiry_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['members.id'], name=op.f('fk_actives_user_id_members')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_actives'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('actives')
    # ### end Alembic commands ###
