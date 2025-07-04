"""Add is_approved to User

Revision ID: 60aeba74ceaf
Revises: 5820cc7322c6
Create Date: 2025-06-20 12:16:24.807209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '60aeba74ceaf'
down_revision = '5820cc7322c6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_approved', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('is_approved')

    # ### end Alembic commands ###
