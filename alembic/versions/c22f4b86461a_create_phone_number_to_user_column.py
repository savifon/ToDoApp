"""Create phone number to user column

Revision ID: c22f4b86461a
Revises: 
Create Date: 2025-02-28 15:28:10.678666

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c22f4b86461a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(),
                                     nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
