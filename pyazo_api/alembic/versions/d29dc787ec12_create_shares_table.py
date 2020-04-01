"""create shares table

Revision ID: d29dc787ec12
Revises: 29dfe923c3ed
Create Date: 2020-04-01 17:56:33.261123

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd29dc787ec12'
down_revision = '29dfe923c3ed'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'shares',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('image_id', sa.Integer),
        sa.Column('user_id', sa.Integer),
    )
    op.create_foreign_key(u'FK_share_user', 'shares', 'users', ['user_id'], ['id'])
    op.create_foreign_key(u'FK_share_image', 'shares', 'images', ['image_id'], ['id'])
    op.create_unique_constraint("UNIQUE_image_user", "shares", ["image_id", "user_id"])


def downgrade():
    pass
