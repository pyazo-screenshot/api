"""add created at field to images table

Revision ID: bf84b9a0b35f
Revises: 29dfe923c3ed
Create Date: 2020-05-14 20:15:09.046821

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
from sqlalchemy import Column, TIMESTAMP, func, DateTime

revision = 'bf84b9a0b35f'
down_revision = '29dfe923c3ed'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'images',
        Column('created_at', DateTime, server_default=func.now())
    )


def downgrade():
    op.drop_column(
        'images',
        'created_at'
    )
