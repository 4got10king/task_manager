import asyncio

from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import pool
from alembic import context

from database.db_metadata import Base

# ruff: noqa: F403
from database.models import *  # Необходимо без этого алембик не видит обновления таблиц.

config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_URL", "sqlite+aiosqlite:///../database.db")


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=Base.metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=Base.metadata,
        render_as_batch=True,  # Важно для SQLite, чтобы правильно работали ALTER TABLE
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={"check_same_thread": False},  # Важно для SQLite
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
