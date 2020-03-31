"""Added private image

Revision ID: 29dfe923c3ed
Revises: 530dca8e7ee4
Create Date: 2020-03-31 15:02:41.770941

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '29dfe923c3ed'
down_revision = '530dca8e7ee4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('images', sa.Column('private', sa.Boolean(), nullable=True))

def downgrade():
    op.drop_column('images', 'private')