"""fix_schema

Revision ID: c721db7d206c
Revises: b29f329ad82b
Create Date: 2026-04-03 10:58:59.592510

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c721db7d206c'
down_revision: Union[str, None] = 'b29f329ad82b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
