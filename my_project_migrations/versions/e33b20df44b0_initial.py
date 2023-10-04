"""initial

Revision ID: e33b20df44b0
Revises: 
Create Date: 2023-10-04 22:07:58.611623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e33b20df44b0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tokens')
    op.add_column('gallery', sa.Column('name', sa.String(), nullable=True))
    op.add_column('gallery', sa.Column('image_data', sa.String(), nullable=True))
    op.add_column('gallery', sa.Column('owner_id', sa.Integer(), nullable=True))
    op.add_column('gallery', sa.Column('created', sa.DateTime(), nullable=True))
    op.add_column('gallery', sa.Column('updated', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_gallery_id'), 'gallery', ['id'], unique=False)
    op.create_index(op.f('ix_gallery_name'), 'gallery', ['name'], unique=False)
    op.create_foreign_key(None, 'gallery', 'users', ['owner_id'], ['id'])
    op.drop_column('users', 'profile_picture')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('profile_picture', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'gallery', type_='foreignkey')
    op.drop_index(op.f('ix_gallery_name'), table_name='gallery')
    op.drop_index(op.f('ix_gallery_id'), table_name='gallery')
    op.drop_column('gallery', 'updated')
    op.drop_column('gallery', 'created')
    op.drop_column('gallery', 'owner_id')
    op.drop_column('gallery', 'image_data')
    op.drop_column('gallery', 'name')
    op.create_table('tokens',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id', name='tokens_pkey')
    )
    # ### end Alembic commands ###