"""First migration

Revision ID: b52b3c48d502
Revises: 
Create Date: 2025-02-05 15:21:36.406361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b52b3c48d502'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('tg_id', sa.BigInteger(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('tg_id')
    )
    op.create_table('incidents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('time', sa.DateTime(), nullable=False),
    sa.Column('hosp_name', sa.String(), nullable=False),
    sa.Column('inc_number', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('resolution', sa.String(), nullable=False),
    sa.Column('restart_platform', sa.Boolean(), nullable=False),
    sa.Column('creator', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['creator'], ['users.tg_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('incidents')
    op.drop_table('users')
    # ### end Alembic commands ###
