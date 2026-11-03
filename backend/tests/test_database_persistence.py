from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base
from main import seed_data
from models import Customer, Device, RepairOrder, SparePart, StatusHistory


def test_records_survive_database_engine_restart(tmp_path):
    database_url = f"sqlite:///{tmp_path / 'persistent.db'}"
    engine_one = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine_one)
    FirstSession = sessionmaker(bind=engine_one, autocommit=False, autoflush=False)

    with FirstSession() as db:
        customer = Customer(name="Persistent Customer", phone="123456")
        device = Device(customer=customer, device_type="Laptop", model="Persistent Laptop")
        order = RepairOrder(
            id="FF-2000",
            customer=customer,
            device=device,
            problem="Test persistence after restart",
            received_date=date(2026, 10, 22),
            status="Diagnosing",
            technician="Test Tech",
            estimated_cost=5000,
            notes="This record should stay in SQLite.",
        )
        order.history.append(
            StatusHistory(status="Diagnosing", changed_at="2026-10-22 10:00")
        )
        db.add(order)
        db.add(SparePart(id="PT-77", name="Saved part", stock=4, unit_price=900))
        db.commit()

    engine_one.dispose()

    # Open the same SQLite file with a new engine/session, like a restarted server.
    engine_two = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine_two)
    SecondSession = sessionmaker(bind=engine_two, autocommit=False, autoflush=False)

    with SecondSession() as db:
        stored_order = db.get(RepairOrder, "FF-2000")
        assert stored_order is not None
        assert stored_order.customer.name == "Persistent Customer"
        assert stored_order.device.model == "Persistent Laptop"
        assert stored_order.history[0].status == "Diagnosing"
        assert db.get(SparePart, "PT-77").stock == 4

        # Application startup should not replace existing data with the demo seed.
        seed_data(db)
        assert db.query(RepairOrder).count() == 1
        assert db.get(RepairOrder, "FF-2000") is not None

    engine_two.dispose()
