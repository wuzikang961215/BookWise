import os
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

# ✅ Step 1: Load environment variables
from dotenv import load_dotenv
load_dotenv()

# ✅ Step 2: Import your model's Base metadata
from app.models.models import Base  # adjust if needed

# ✅ Alembic config
config = context.config

# ✅ Step 3: Inject DATABASE_URL from .env into alembic config
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# ✅ Set the metadata for autogenerate to work
target_metadata = Base.metadata

# ✅ Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- No changes below this line ---

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
