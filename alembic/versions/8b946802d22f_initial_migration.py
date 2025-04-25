"""initial migration

Revision ID: 8b946802d22f
Revises: 
Create Date: 2025-04-07 16:35:53.815226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8b946802d22f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Criação da tabela users
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(), unique=True),
        sa.Column('username', sa.String(), unique=True),
        sa.Column('first_name', sa.String()),
        sa.Column('last_name', sa.String()),
        sa.Column('hashed_password', sa.String()),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('role', sa.String()),
        sa.Column('phone_number', sa.String()),
    )

    # Criação da tabela todos
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('title', sa.String()),
        sa.Column('description', sa.String()),
        sa.Column('priority', sa.Integer()),
        sa.Column('complete', sa.Boolean(), default=False),
        sa.Column('owner_id', sa.Integer(), sa.ForeignKey('users.id')),
    )


def downgrade():
    # Exclusão das tabelas na ordem inversa
    op.drop_table('todos')
    op.drop_table('users')
