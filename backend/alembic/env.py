from alembic import context
from sqlalchemy import create_engine, pool

from database import DATABASE_URL, Base, normalize_database_url
import models  # noqa: F401  (importing the models registers the tables)

config = context.config
target_metadata = Base.metadata


def get_url() -> str:
    # A URL set on the Alembic config (used by tests) wins over DATABASE_URL.
    return normalize_database_url(config.get_main_option("sqlalchemy.url") or DATABASE_URL)


def run_migrations_offline() -> None:
    context.configure(url=get_url(), target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = get_url()
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    engine = create_engine(url, poolclass=pool.NullPool, connect_args=connect_args)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()
    engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
