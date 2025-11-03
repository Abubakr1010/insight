"""update otp table

Revision ID: ec68e1764c58
Revises: 0d818d830b0a
Create Date: 2025-11-03 19:55:17.550821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ec68e1764c58'
down_revision: Union[str, Sequence[str], None] = '0d818d830b0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
