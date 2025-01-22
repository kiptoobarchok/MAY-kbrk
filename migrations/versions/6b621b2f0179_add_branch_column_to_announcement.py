"""Add branch column to Announcement

Revision ID: 6b621b2f0179
Revises: 30c00ac45088
Create Date: 2025-01-23 01:47:46.708692

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6b621b2f0179'
down_revision = '30c00ac45088'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('announcement', schema=None) as batch_op:
        batch_op.add_column(sa.Column('branch', sa.String(length=50), nullable=False))


def downgrade():
    with op.batch_alter_table('announcement', schema=None) as batch_op:
        batch_op.drop_column('branch')
    # ### end Alembic commands ###
