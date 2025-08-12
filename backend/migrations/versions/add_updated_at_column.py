"""Add updated_at column to orders table

Revision ID: add_updated_at_column
Revises: c7cd5e23b57a
Create Date: 2025-08-12 17:21:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_updated_at_column'
down_revision = 'c7cd5e23b57a'
branch_labels = None
depends_on = None


def upgrade():
    # Add updated_at column to orders table
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True))
    
    # Set default value for existing records (outside the batch operation)
    op.execute("UPDATE orders SET updated_at = created_at")
    
    # Make it not nullable after setting default values
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.alter_column('updated_at', nullable=False)


def downgrade():
    # Remove updated_at column from orders table
    with op.batch_alter_table('orders', schema=None) as batch_op:
        batch_op.drop_column('updated_at')
