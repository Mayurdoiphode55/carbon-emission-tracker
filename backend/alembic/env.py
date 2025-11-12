from __future__ import with_statement
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
# add app package to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
fileConfig(config.config_file_name)

# Import your models' MetaData object here for 'autogenerate'
from app.db import Base  # Base is declarative_base()
from app import models     # ensure models are imported so that metadata is populated

target_metadata = Base.metadata

# set sqlalchemy.url dynamically from .env
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL not set in .env for alembic")

config.set_main_option("sqlalchemy.url", db_url)


def run_migrations_offline():
    context.configure(
        url=db_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
