"""create users and stores tables

Revision ID: 0d818d830b0a
Revises: 
Create Date: 2025-10-25 16:04:39.599022
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '0d818d830b0a'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=False),
        sa.Column("password_hash", sa.String, nullable=False),
        sa.Column("is_active", sa.Boolean, server_default=sa.text("TRUE")),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "stores",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("shop_domain", sa.String, unique=True, nullable=False),
        sa.Column("access_token", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
    )

    op.create_table(
        "user_otps",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("otp_code", sa.String, nullable=False),
        sa.Column("expires_at", sa.TIMESTAMP, nullable=False),
        sa.Column("used", sa.Boolean, server_default=sa.text("FALSE")),
        sa.Column("created_at", sa.TIMESTAMP, server_default=sa.text("CURRENT_TIMESTAMP")),
    )


def downgrade():
    op.drop_table("user_otps") # fix op.drop_table("user_otps")   
    op.drop_table("stores")
    op.drop_table("users")
