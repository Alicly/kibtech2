"""add news fields migration

Revision ID: add_news_fields_migration
Revises: 1de6efc77b1d
Create Date: 2025-06-24 12:40:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_news_fields_migration'
down_revision = '1de6efc77b1d'
branch_labels = None
depends_on = None


def upgrade():
    # Add new columns to news table
    op.add_column('news', sa.Column('category', sa.String(50), nullable=True))
    op.add_column('news', sa.Column('author', sa.String(100), nullable=True))
    op.add_column('news', sa.Column('views', sa.Integer(), nullable=True, server_default='0'))
    
    # Set default values for existing rows
    op.execute("UPDATE news SET category = 'general' WHERE category IS NULL")
    op.execute("UPDATE news SET views = 0 WHERE views IS NULL")


def downgrade():
    # Remove the columns
    op.drop_column('news', 'category')
    op.drop_column('news', 'author')
    op.drop_column('news', 'views') 