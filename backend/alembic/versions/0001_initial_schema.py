"""Create the FixFlow tables.

Revision ID: 0001
Revises:
Create Date: 2026-11-03
"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Each table is created only if it is missing, so this also works on a database
    # that was created earlier by the app itself (for example an old SQLite file).
    existing = set(sa.inspect(op.get_bind()).get_table_names())

    if "customers" not in existing:
        op.create_table(
            "customers",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("name", sa.String(120), nullable=False),
            sa.Column("phone", sa.String(50), nullable=False),
        )
        op.create_index("ix_customers_id", "customers", ["id"])

    if "devices" not in existing:
        op.create_table(
            "devices",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("customer_id", sa.Integer(), sa.ForeignKey("customers.id"), nullable=False),
            sa.Column("device_type", sa.String(50), nullable=False),
            sa.Column("model", sa.String(150), nullable=False),
        )
        op.create_index("ix_devices_id", "devices", ["id"])

    if "repair_orders" not in existing:
        op.create_table(
            "repair_orders",
            sa.Column("id", sa.String(20), primary_key=True),
            sa.Column("customer_id", sa.Integer(), sa.ForeignKey("customers.id"), nullable=False),
            sa.Column("device_id", sa.Integer(), sa.ForeignKey("devices.id"), nullable=False),
            sa.Column("problem", sa.Text(), nullable=False),
            sa.Column("received_date", sa.Date(), nullable=False),
            sa.Column("status", sa.String(40), nullable=False),
            sa.Column("technician", sa.String(100), nullable=False),
            sa.Column("estimated_cost", sa.Float(), nullable=True),
            sa.Column("notes", sa.Text(), nullable=False),
        )

    if "status_history" not in existing:
        op.create_table(
            "status_history",
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("order_id", sa.String(20), sa.ForeignKey("repair_orders.id"), nullable=False),
            sa.Column("status", sa.String(40), nullable=False),
            sa.Column("changed_at", sa.String(30), nullable=False),
        )
        op.create_index("ix_status_history_id", "status_history", ["id"])

    if "spare_parts" not in existing:
        op.create_table(
            "spare_parts",
            sa.Column("id", sa.String(20), primary_key=True),
            sa.Column("name", sa.String(120), nullable=False),
            sa.Column("stock", sa.Integer(), nullable=False),
            sa.Column("unit_price", sa.Float(), nullable=False),
        )


def downgrade() -> None:
    op.drop_table("spare_parts")
    op.drop_table("status_history")
    op.drop_table("repair_orders")
    op.drop_table("devices")
    op.drop_table("customers")
