"""create images table

Revision ID: 530dca8e7ee4
Revises: cb397364ed10
Create Date: 2020-03-19 23:00:25.873068

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '530dca8e7ee4'
down_revision = 'cb397364ed10'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'images',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer),
        sa.Column('path', sa.String(128), nullable=False),
    )
    op.create_foreign_key(u'FK_image_user', 'images', 'users', ['owner_id'], ['id'])


def downgrade():
    op.drop_table('images')
