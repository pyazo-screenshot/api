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
    op.create_table(
        'shares',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('image_id', sa.String),
        sa.Column('user_id', sa.Integer),
    )
    op.create_foreign_key(u'FK_share_user', 'shares', 'users', ['user_id'], ['id'])
    op.create_foreign_key(u'FK_share_image', 'shares', 'images', ['image_id'], ['id'])
    op.create_unique_constraint("UNIQUE_image_user", "shares", ["image_id", "user_id"])


def downgrade():
    op.drop_table('shares')
