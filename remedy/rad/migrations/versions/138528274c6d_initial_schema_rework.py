"""Initial schema rework.

Revision ID: 138528274c6d
Revises: None
Create Date: 2014-09-05 21:35:55.050000

"""

# revision identifiers, used by Alembic.
revision = '138528274c6d'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=100), nullable=False),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('resource',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.Unicode(length=250), nullable=False),
    sa.Column('organization', sa.Unicode(length=500), nullable=True),
    sa.Column('description', sa.UnicodeText(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.Column('address', sa.Unicode(length=500), nullable=True),
    sa.Column('latitude', sa.Float(), nullable=True),
    sa.Column('longitude', sa.Float(), nullable=True),
    sa.Column('email', sa.Unicode(length=250), nullable=True),
    sa.Column('phone', sa.Unicode(length=50), nullable=True),
    sa.Column('fax', sa.Unicode(length=50), nullable=True),
    sa.Column('url', sa.Unicode(length=500), nullable=True),
    sa.Column('source', sa.UnicodeText(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('last_updated', sa.DateTime(), nullable=False),
    sa.Column('category_text', sa.UnicodeText(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.Unicode(length=50), nullable=False),
    sa.Column('password', sa.Unicode(length=128), server_default='', nullable=False),
    sa.Column('email', sa.Unicode(length=250), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('default_location', sa.Unicode(length=500), nullable=True),
    sa.Column('default_latitude', sa.Float(), nullable=True),
    sa.Column('default_longitude', sa.Float(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('resourcecategory',
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], ),
    sa.PrimaryKeyConstraint('resource_id', 'category_id')
    )
    op.create_table('review',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.UnicodeText(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('visible', sa.Boolean(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('resource_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['resource_id'], ['resource.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('review')
    op.drop_table('resourcecategory')
    op.drop_table('user')
    op.drop_table('resource')
    op.drop_table('category')
    ### end Alembic commands ###
