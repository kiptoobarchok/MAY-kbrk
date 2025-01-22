"""Add branch column to Announcement

Revision ID: 30c00ac45088
Revises: b267225b51fe
Create Date: 2025-01-23 01:39:28.221602

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30c00ac45088'
down_revision = 'b267225b51fe'
branch_labels = None
depends_on = None


def upgrade():
    # Add the 'branch' column to the 'announcement' table
    with op.batch_alter_table('announcement', schema=None) as batch_op:
        batch_op.add_column(sa.Column('branch', sa.String(length=50), nullable=False))


def downgrade():
    # Remove the 'branch' column from the 'announcement' table
    with op.batch_alter_table('announcement', schema=None) as batch_op:
        batch_op.drop_column('branch')
