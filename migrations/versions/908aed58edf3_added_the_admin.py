"""Added the admin

Revision ID: 908aed58edf3
Revises: ebe3cc8da836
Create Date: 2025-01-08 19:50:39.893234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '908aed58edf3'
down_revision = 'ebe3cc8da836'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('admins',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=60), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_admins')),
    sa.UniqueConstraint('email', name=op.f('uq_admins_email'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('admins')
    # ### end Alembic commands ###
