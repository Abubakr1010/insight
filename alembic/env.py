from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os

# --- Alembic Config ---
config = context.config

# --- Logging ---
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- Use DATABASE_URL from environment ---
def get_url():
    return os.getenv("DATABASE_URL", config.get_main_option("sqlalchemy.url"))

# --- Migration functions ---
def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        # Alembic will execute the SQL statements in your migration files
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        url=get_url(),
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection)

        with context.begin_transaction():
            # Alembic will execute the SQL statements in your migration files
            context.run_migrations()


# --- Run the appropriate mode ---
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
