"""correctly remove profile table

Revision ID: 940d06bf07a6
Revises: b36f541df7e9
Create Date: 2025-01-27 13:41:04.548685

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '940d06bf07a6'
down_revision: Union[str, None] = 'b36f541df7e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
