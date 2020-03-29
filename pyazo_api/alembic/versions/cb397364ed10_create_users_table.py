"""create users table

Revision ID: cb397364ed10
Revises:
Create Date: 2020-03-19 22:59:33.147253

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb397364ed10'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('hashed_password', sa.Unicode(200), nullable=False),
    )


def downgrade():
    op.drop_table('account')
