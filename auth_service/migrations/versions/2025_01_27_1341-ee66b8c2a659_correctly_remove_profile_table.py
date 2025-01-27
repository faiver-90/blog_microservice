"""correctly remove profile table

Revision ID: ee66b8c2a659
Revises: 940d06bf07a6
Create Date: 2025-01-27 13:41:14.862769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee66b8c2a659'
down_revision: Union[str, None] = '940d06bf07a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
