"""create phone number to user column

Revision ID: a4f9263f0a43
Revises: 8b946802d22f
Create Date: 2025-04-07 16:41:32.383519

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4f9263f0a43'
down_revision: Union[str, None] = '8b946802d22f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(),
                                     nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
