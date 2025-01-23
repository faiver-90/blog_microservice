"""empty message

Revision ID: c7ef212494f8
Revises: 65e1ef447bb5
Create Date: 2025-01-22 14:06:56.684731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7ef212494f8'
down_revision: Union[str, None] = '65e1ef447bb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
