"""correctly remove profile table

Revision ID: 1fea7f6676f2
Revises: ee66b8c2a659
Create Date: 2025-01-27 13:43:31.101609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1fea7f6676f2'
down_revision: Union[str, None] = 'ee66b8c2a659'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
