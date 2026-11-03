from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import Base, SessionLocal, engine, get_db
from models import Customer, Device, RepairOrder as RepairOrderRow, SparePart as SparePartRow, StatusHistory


class RepairStatus(str, Enum):
    received = "Received"
    diagnosing = "Diagnosing"
    waiting_for_parts = "Waiting for parts"
    repairing = "Repairing"
    ready_for_pickup = "Ready for pickup"
    completed = "Completed"
    cancelled = "Cancelled"


class StatusHistoryEntry(BaseModel):
    status: RepairStatus
    date: str


class RepairOrderInput(BaseModel):
    customerName: str = Field(min_length=1)
    phone: str = ""
    deviceType: str = "Laptop"
    deviceModel: str = Field(min_length=1)
    problem: str = Field(min_length=1)
    receivedDate: date
    status: RepairStatus
    technician: str = ""
    estimatedCost: Optional[float] = Field(default=None, ge=0)
    notes: str = ""

    @field_validator("customerName", "deviceModel", "problem")
    @classmethod
    def required_text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("This field cannot be empty")
        return value.strip()


class RepairOrder(RepairOrderInput):
    id: str
    history: list[StatusHistoryEntry]


class StatusChange(BaseModel):
    status: RepairStatus


class SparePartInput(BaseModel):
    name: str = Field(min_length=1)
    stock: int = Field(ge=0)
    unitPrice: float = Field(ge=0)

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Part name cannot be empty")
        return value.strip()


class SparePart(BaseModel):
    id: str
    name: str
    stock: int
    unitPrice: float


class PublicOrderStatus(BaseModel):
    id: str
    deviceModel: str
    receivedDate: date
    status: RepairStatus
    message: str


PUBLIC_MESSAGES = {
    "Received": "Your device has been received and is waiting for a technician.",
    "Diagnosing": "A technician is checking your device to find the problem.",
    "Waiting for parts": "The repair is waiting for the required part to arrive.",
    "Repairing": "The repair is in progress.",
    "Ready for pickup": "Your device is ready. Please contact the shop to arrange pickup.",
    "Completed": "This repair has been completed.",
    "Cancelled": "This repair order has been cancelled.",
}


def now_text() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def starter_orders() -> list[dict]:
    return [
        {"id": "FF-1001", "customerName": "Aigerim S.", "phone": "+7 701 123 45 67", "deviceType": "Laptop", "deviceModel": "ASUS TUF Gaming A15", "problem": "Laptop gets too hot and shuts down.", "receivedDate": "2026-10-20", "status": "Diagnosing", "technician": "Arman", "estimatedCost": 12000, "notes": "Check cooling system and clean fans.", "history": [{"status": "Received", "date": "2026-10-20 10:20"}, {"status": "Diagnosing", "date": "2026-10-21 09:15"}]},
        {"id": "FF-1002", "customerName": "Daniyar K.", "phone": "+7 707 555 11 22", "deviceType": "Laptop", "deviceModel": "MacBook Air M1", "problem": "Battery does not hold charge for long.", "receivedDate": "2026-10-19", "status": "Waiting for parts", "technician": "Nursultan", "estimatedCost": 28000, "notes": "Waiting for a compatible battery.", "history": [{"status": "Received", "date": "2026-10-19 12:05"}, {"status": "Waiting for parts", "date": "2026-10-20 11:30"}]},
        {"id": "FF-1003", "customerName": "Madina A.", "phone": "+7 747 444 22 00", "deviceType": "Phone", "deviceModel": "iPhone 13", "problem": "Charging port is loose.", "receivedDate": "2026-10-18", "status": "Ready for pickup", "technician": "Arman", "estimatedCost": 18000, "notes": "Repair completed. Customer can pick it up.", "history": [{"status": "Received", "date": "2026-10-18 11:10"}, {"status": "Ready for pickup", "date": "2026-10-20 17:00"}]},
        {"id": "FF-1004", "customerName": "Timur B.", "phone": "+7 775 222 33 44", "deviceType": "Laptop", "deviceModel": "Lenovo IdeaPad 5", "problem": "Screen flickers when moving the lid.", "receivedDate": "2026-10-17", "status": "Repairing", "technician": "Nursultan", "estimatedCost": 22000, "notes": "Checking the display cable.", "history": [{"status": "Received", "date": "2026-10-17 09:40"}, {"status": "Repairing", "date": "2026-10-18 10:00"}]},
        {"id": "FF-1005", "customerName": "Alina R.", "phone": "+7 702 888 77 66", "deviceType": "Tablet", "deviceModel": "iPad 9th Gen", "problem": "Glass is cracked.", "receivedDate": "2026-10-15", "status": "Completed", "technician": "Arman", "estimatedCost": 35000, "notes": "Picked up by the customer.", "history": [{"status": "Received", "date": "2026-10-15 16:45"}, {"status": "Completed", "date": "2026-10-17 13:00"}]},
    ]


def starter_parts() -> list[dict]:
    return [
        {"id": "PT-01", "name": "Laptop fan", "stock": 6, "unitPrice": 4500},
        {"id": "PT-02", "name": "USB-C charging port", "stock": 10, "unitPrice": 2200},
        {"id": "PT-03", "name": "Thermal paste", "stock": 14, "unitPrice": 1800},
        {"id": "PT-04", "name": "Laptop battery", "stock": 2, "unitPrice": 18000},
    ]


def seed_data(db: Session) -> None:
    if db.query(RepairOrderRow).count() > 0:
        return
    for item in starter_orders():
        customer = Customer(name=item["customerName"], phone=item["phone"])
        device = Device(customer=customer, device_type=item["deviceType"], model=item["deviceModel"])
        order = RepairOrderRow(
            id=item["id"], customer=customer, device=device, problem=item["problem"],
            received_date=date.fromisoformat(item["receivedDate"]), status=item["status"],
            technician=item["technician"], estimated_cost=item["estimatedCost"], notes=item["notes"],
        )
        db.add(order)
        for entry in item["history"]:
            order.history.append(StatusHistory(status=entry["status"], changed_at=entry["date"]))
    for item in starter_parts():
        db.add(SparePartRow(id=item["id"], name=item["name"], stock=item["stock"], unit_price=item["unitPrice"]))
    db.commit()


def order_to_dict(order: RepairOrderRow) -> dict:
    return {
        "id": order.id,
        "customerName": order.customer.name,
        "phone": order.customer.phone,
        "deviceType": order.device.device_type,
        "deviceModel": order.device.model,
        "problem": order.problem,
        "receivedDate": order.received_date.isoformat(),
        "status": order.status,
        "technician": order.technician,
        "estimatedCost": order.estimated_cost,
        "notes": order.notes,
        "history": [{"status": item.status, "date": item.changed_at} for item in order.history],
    }


def part_to_dict(part: SparePartRow) -> dict:
    return {"id": part.id, "name": part.name, "stock": part.stock, "unitPrice": part.unit_price}


def next_order_id(db: Session) -> str:
    ids = [row[0] for row in db.query(RepairOrderRow.id).all()]
    numbers = [int(value.replace("FF-", "")) for value in ids if value.startswith("FF-")]
    return f"FF-{max([1000, *numbers]) + 1}"


def next_part_id(db: Session) -> str:
    ids = [row[0] for row in db.query(SparePartRow.id).all()]
    numbers = [int(value.replace("PT-", "")) for value in ids if value.startswith("PT-")]
    return f"PT-{max([0, *numbers]) + 1:02d}"


def find_order(db: Session, order_id: str) -> RepairOrderRow:
    order = db.get(RepairOrderRow, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Repair order not found")
    return order


app = FastAPI(title="FixFlow API", version="1.0.0", description="A simple repair shop API.")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"https://[a-z0-9-]+-5173\.app\.github\.dev",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/orders", response_model=list[RepairOrder])
def list_repair_orders(search: str = Query(default=""), status_filter: Optional[RepairStatus] = Query(default=None, alias="status"), db: Session = Depends(get_db)) -> list[dict]:
    query = db.query(RepairOrderRow).join(Customer).join(Device)
    term = search.strip()
    if term:
        like = f"%{term}%"
        query = query.filter(or_(RepairOrderRow.id.ilike(like), Customer.name.ilike(like), Device.model.ilike(like)))
    if status_filter:
        query = query.filter(RepairOrderRow.status == status_filter.value)
    result = query.order_by(RepairOrderRow.received_date.desc(), RepairOrderRow.id.asc()).all()
    return [order_to_dict(order) for order in result]


@app.post("/orders", response_model=RepairOrder, status_code=status.HTTP_201_CREATED)
def create_repair_order(payload: RepairOrderInput, db: Session = Depends(get_db)) -> dict:
    data = payload.model_dump(mode="json")
    customer = Customer(name=data["customerName"], phone=data["phone"])
    device = Device(customer=customer, device_type=data["deviceType"], model=data["deviceModel"])
    order = RepairOrderRow(
        id=next_order_id(db), customer=customer, device=device, problem=data["problem"],
        received_date=date.fromisoformat(data["receivedDate"]), status=data["status"],
        technician=data["technician"], estimated_cost=data["estimatedCost"], notes=data["notes"],
    )
    order.history.append(StatusHistory(status=data["status"], changed_at=now_text()))
    db.add(order)
    db.commit()
    db.refresh(order)
    return order_to_dict(order)


@app.get("/orders/{order_id}", response_model=RepairOrder)
def get_repair_order(order_id: str, db: Session = Depends(get_db)) -> dict:
    return order_to_dict(find_order(db, order_id))


@app.patch("/orders/{order_id}", response_model=RepairOrder)
def edit_repair_order(order_id: str, payload: RepairOrderInput, db: Session = Depends(get_db)) -> dict:
    order = find_order(db, order_id)
    data = payload.model_dump(mode="json")
    old_status = order.status
    order.customer.name = data["customerName"]
    order.customer.phone = data["phone"]
    order.device.device_type = data["deviceType"]
    order.device.model = data["deviceModel"]
    order.problem = data["problem"]
    order.received_date = date.fromisoformat(data["receivedDate"])
    order.status = data["status"]
    order.technician = data["technician"]
    order.estimated_cost = data["estimatedCost"]
    order.notes = data["notes"]
    if old_status != order.status:
        order.history.append(StatusHistory(status=order.status, changed_at=now_text()))
    db.commit()
    db.refresh(order)
    return order_to_dict(order)


@app.patch("/orders/{order_id}/status", response_model=RepairOrder)
def change_repair_status(order_id: str, payload: StatusChange, db: Session = Depends(get_db)) -> dict:
    order = find_order(db, order_id)
    order.status = payload.status.value
    order.history.append(StatusHistory(status=order.status, changed_at=now_text()))
    db.commit()
    db.refresh(order)
    return order_to_dict(order)


@app.get("/parts", response_model=list[SparePart])
def list_spare_parts(db: Session = Depends(get_db)) -> list[dict]:
    return [part_to_dict(part) for part in db.query(SparePartRow).order_by(SparePartRow.id).all()]


@app.post("/parts", response_model=SparePart, status_code=status.HTTP_201_CREATED)
def create_spare_part(payload: SparePartInput, db: Session = Depends(get_db)) -> dict:
    data = payload.model_dump()
    part = SparePartRow(id=next_part_id(db), name=data["name"], stock=data["stock"], unit_price=data["unitPrice"])
    db.add(part)
    db.commit()
    db.refresh(part)
    return part_to_dict(part)


@app.patch("/parts/{part_id}", response_model=SparePart)
def edit_spare_part(part_id: str, payload: SparePartInput, db: Session = Depends(get_db)) -> dict:
    part = db.get(SparePartRow, part_id)
    if part is None:
        raise HTTPException(status_code=404, detail="Spare part not found")
    data = payload.model_dump()
    part.name = data["name"]
    part.stock = data["stock"]
    part.unit_price = data["unitPrice"]
    db.commit()
    db.refresh(part)
    return part_to_dict(part)


@app.get("/public/orders/{order_id}", response_model=PublicOrderStatus)
def get_public_order_status(order_id: str, db: Session = Depends(get_db)) -> dict:
    order = db.get(RepairOrderRow, order_id.upper())
    if order is None:
        raise HTTPException(status_code=404, detail="Repair order not found")
    return {
        "id": order.id,
        "deviceModel": order.device.model,
        "receivedDate": order.received_date.isoformat(),
        "status": order.status,
        "message": PUBLIC_MESSAGES[order.status],
    }


# Serve the web app from the API origin in Codespaces. This keeps browser API
# calls same-origin and avoids cross-origin restrictions on forwarded ports.
FRONTEND_DIR = Path(__file__).resolve().parent.parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
