"""Copy all FixFlow data from a SQLite file into PostgreSQL.

Run the Alembic migrations on the PostgreSQL database first (`alembic upgrade head`
in the backend folder), then run:

    python scripts/migrate_sqlite_to_postgres.py \
        --source sqlite:///backend/fixflow.db \
        --target postgresql://fixflow:fixflow@localhost:5432/fixflow

The script keeps the original IDs and copies only rows that are not in the target yet,
so it is safe to run more than once.
"""
import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from sqlalchemy import Integer, create_engine, inspect, select, text  # noqa: E402

from database import Base, normalize_database_url  # noqa: E402
import models  # noqa: E402,F401  (importing the models registers the tables)


def copy_data(source_url: str, target_url: str) -> dict:
    """Copy every table from source to target and return how many rows were added per table."""
    source = create_engine(normalize_database_url(source_url))
    target = create_engine(normalize_database_url(target_url))
    tables = Base.metadata.sorted_tables  # parents before children, so foreign keys are valid

    target_tables = inspect(target)
    missing = [table.name for table in tables if not target_tables.has_table(table.name)]
    if missing:
        raise SystemExit(f"Missing tables in the target database: {', '.join(missing)}. Run `alembic upgrade head` first.")

    added = {}
    with source.connect() as source_connection, target.begin() as target_connection:
        for table in tables:
            key = list(table.primary_key.columns)[0]
            already_there = {row[0] for row in target_connection.execute(select(key))}
            rows = [dict(row._mapping) for row in source_connection.execute(select(table).order_by(key))]
            new_rows = [row for row in rows if row[key.name] not in already_there]
            if new_rows:
                target_connection.execute(table.insert(), new_rows)
            added[table.name] = len(new_rows)

        if target.dialect.name == "postgresql":
            # We inserted IDs by hand, so move each ID counter past the highest copied ID.
            for table in tables:
                key = list(table.primary_key.columns)[0]
                if isinstance(key.type, Integer):
                    target_connection.execute(text(
                        f"SELECT setval(pg_get_serial_sequence('{table.name}', '{key.name}'), "
                        f"COALESCE(MAX({key.name}), 1), MAX({key.name}) IS NOT NULL) FROM {table.name}"
                    ))

    source.dispose()
    target.dispose()
    return added


def main() -> None:
    parser = argparse.ArgumentParser(description="Copy FixFlow data from SQLite to PostgreSQL.")
    parser.add_argument("--source", default="sqlite:///backend/fixflow.db", help="SQLite database URL")
    parser.add_argument("--target", default=os.getenv("DATABASE_URL"), help="PostgreSQL database URL (default: $DATABASE_URL)")
    args = parser.parse_args()
    if not args.target:
        raise SystemExit("Give the PostgreSQL address with --target or the DATABASE_URL variable.")

    for name, count in copy_data(args.source, args.target).items():
        print(f"{name}: {count} rows copied")


if __name__ == "__main__":
    main()
