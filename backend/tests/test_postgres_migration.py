"""Tests for the Alembic migration and the SQLite -> PostgreSQL copy script.

They need a PostgreSQL database, so they run only when TEST_DATABASE_URL points to one
(GitHub Actions sets it). Without it they are skipped.
"""
import importlib.util
import os
from datetime import date
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, func, inspect, select, text
from sqlalchemy.orm import sessionmaker

from database import Base, normalize_database_url
from main import seed_data
from models import Customer, Device, RepairOrder, SparePart, StatusHistory

POSTGRES_URL = os.getenv("TEST_DATABASE_URL", "")
pytestmark = pytest.mark.skipif(
    not normalize_database_url(POSTGRES_URL).startswith("postgresql"),
    reason="TEST_DATABASE_URL does not point to PostgreSQL",
)

BACKEND = Path(__file__).resolve().parent.parent
SCRIPT = BACKEND.parent / "scripts" / "migrate_sqlite_to_postgres.py"


def load_copy_script():
    spec = importlib.util.spec_from_file_location("migrate_sqlite_to_postgres", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture()
def empty_postgres():
    engine = create_engine(normalize_database_url(POSTGRES_URL))
    with engine.begin() as connection:
        connection.execute(text("DROP SCHEMA public CASCADE"))
        connection.execute(text("CREATE SCHEMA public"))
    yield engine
    engine.dispose()


def run_alembic_upgrade():
    config = Config(str(BACKEND / "alembic.ini"))
    config.set_main_option("sqlalchemy.url", POSTGRES_URL)
    command.upgrade(config, "head")


@pytest.fixture()
def seeded_sqlite(tmp_path):
    url = f"sqlite:///{tmp_path / 'old_fixflow.db'}"
    engine = create_engine(url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    with sessionmaker(bind=engine)() as db:
        seed_data(db)
    engine.dispose()
    return url


def test_alembic_creates_all_tables_on_empty_postgres(empty_postgres):
    run_alembic_upgrade()
    tables = set(inspect(empty_postgres).get_table_names())
    assert {"customers", "devices", "repair_orders", "status_history", "spare_parts", "alembic_version"} <= tables


def test_alembic_upgrade_can_run_twice(empty_postgres):
    run_alembic_upgrade()
    run_alembic_upgrade()
    assert "repair_orders" in inspect(empty_postgres).get_table_names()


def test_sqlite_data_is_copied_with_ids_and_history(empty_postgres, seeded_sqlite):
    run_alembic_upgrade()
    added = load_copy_script().copy_data(seeded_sqlite, POSTGRES_URL)
    assert added["repair_orders"] == 5
    assert added["spare_parts"] == 4
    assert added["status_history"] == 10

    with sessionmaker(bind=empty_postgres)() as db:
        order = db.get(RepairOrder, "FF-1002")
        assert order.customer.name == "Daniyar K."
        assert [item.status for item in order.history] == ["Received", "Waiting for parts"]
        assert db.get(SparePart, "PT-04").stock == 2


def test_running_the_copy_twice_does_not_duplicate_rows(empty_postgres, seeded_sqlite):
    run_alembic_upgrade()
    script = load_copy_script()
    script.copy_data(seeded_sqlite, POSTGRES_URL)
    second = script.copy_data(seeded_sqlite, POSTGRES_URL)
    assert sum(second.values()) == 0
    with empty_postgres.connect() as connection:
        assert connection.execute(select(func.count()).select_from(RepairOrder.__table__)).scalar() == 5


def test_new_rows_can_be_added_after_the_copy(empty_postgres, seeded_sqlite):
    run_alembic_upgrade()
    load_copy_script().copy_data(seeded_sqlite, POSTGRES_URL)
    with sessionmaker(bind=empty_postgres)() as db:
        customer = Customer(name="After Copy", phone="")
        device = Device(customer=customer, device_type="Laptop", model="After Copy Laptop")
        order = RepairOrder(id="FF-2001", customer=customer, device=device, problem="x",
                            received_date=date(2026, 11, 3), status="Received")
        order.technician = ""
        order.notes = ""
        order.history.append(StatusHistory(status="Received", changed_at="2026-11-03 10:00"))
        db.add(order)
        db.commit()  # fails with a duplicate key error if the ID counters were not moved forward
        assert db.query(RepairOrder).count() == 6
