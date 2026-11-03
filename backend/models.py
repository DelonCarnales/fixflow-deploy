from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    phone = Column(String(50), default="", nullable=False)

    devices = relationship("Device", back_populates="customer")
    repair_orders = relationship("RepairOrder", back_populates="customer")


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    device_type = Column(String(50), nullable=False, default="Laptop")
    model = Column(String(150), nullable=False)

    customer = relationship("Customer", back_populates="devices")
    repair_orders = relationship("RepairOrder", back_populates="device")


class RepairOrder(Base):
    __tablename__ = "repair_orders"

    id = Column(String(20), primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)
    problem = Column(Text, nullable=False)
    received_date = Column(Date, nullable=False)
    status = Column(String(40), nullable=False)
    technician = Column(String(100), default="", nullable=False)
    estimated_cost = Column(Float, nullable=True)
    notes = Column(Text, default="", nullable=False)

    customer = relationship("Customer", back_populates="repair_orders")
    device = relationship("Device", back_populates="repair_orders")
    history = relationship(
        "StatusHistory",
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="StatusHistory.id",
    )


class StatusHistory(Base):
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(20), ForeignKey("repair_orders.id"), nullable=False)
    status = Column(String(40), nullable=False)
    changed_at = Column(String(30), nullable=False)

    order = relationship("RepairOrder", back_populates="history")


class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(String(20), primary_key=True)
    name = Column(String(120), nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    unit_price = Column(Float, nullable=False, default=0)
