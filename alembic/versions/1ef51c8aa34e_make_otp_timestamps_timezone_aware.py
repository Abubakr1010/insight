"""make OTP timestamps timezone aware

Revision ID: 1ef51c8aa34e
Revises: ec68e1764c58
Create Date: 2025-12-18 12:48:06.314981

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ef51c8aa34e'
down_revision: Union[str, Sequence[str], None] = 'ec68e1764c58'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # make expires_at timezone-aware
    op.alter_column(
        "user_otps",
        "expires_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="expires_at AT TIME ZONE 'UTC'"
    )

    # make created_at timezone-aware
    op.alter_column(
        "user_otps",
        "created_at",
        type_=sa.TIMESTAMP(timezone=True),
        postgresql_using="created_at AT TIME ZONE 'UTC'"
    )

def downgrade():
    op.alter_column(
        "user_otps",
        "expires_at",
        type_=sa.TIMESTAMP(timezone=False),
        postgresql_using="expires_at AT TIME ZONE 'UTC'"
    )
    op.alter_column(
        "user_otps",
        "created_at",
        type_=sa.TIMESTAMP(timezone=False),
        postgresql_using="created_at AT TIME ZONE 'UTC'"
    )