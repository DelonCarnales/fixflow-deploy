import os
import time
from uuid import uuid4
import httpx
import psycopg2

BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:8000").rstrip("/")
DATABASE_URL = os.getenv("TEST_DATABASE_URL", "postgresql://fixflow:fixflow@localhost:5432/fixflow")

def wait_for_app():
    last_error = None
    for _ in range(60):
        try:
            response = httpx.get(f"{BASE_URL}/health", timeout=3)
            if response.status_code == 200: return
        except httpx.HTTPError as exc: last_error = exc
        time.sleep(2)
    raise AssertionError(f"Application did not become healthy: {last_error}")

def test_compose_serves_frontend_and_health():
    wait_for_app()
    for path in ("/", "/styles.css", "/src/app.js"):
        response = httpx.get(f"{BASE_URL}{path}", timeout=10)
        assert response.status_code == 200, path
    assert httpx.get(f"{BASE_URL}/health").json() == {"status": "ok"}

def test_api_writes_order_to_postgres():
    wait_for_app()
    marker = uuid4().hex[:10]
    payload = {"customerName": f"Integration {marker}", "phone": "+7 700 000 00 00", "deviceType": "Laptop", "deviceModel": f"Integration device {marker}", "problem": "Compose integration persistence", "receivedDate": "2026-11-03", "status": "Received", "technician": "CI", "estimatedCost": 1000, "notes": marker}
    response = httpx.post(f"{BASE_URL}/orders", json=payload, timeout=10)
    assert response.status_code == 201, response.text
    order_id = response.json()["id"]
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT notes FROM repair_orders WHERE id = %s", (order_id,))
            row = cursor.fetchone()
    assert row == (marker,)

def test_compose_database_has_migrated_tables():
    wait_for_app()
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            tables = {row[0] for row in cursor.fetchall()}
    assert {"customers", "devices", "repair_orders", "status_history", "spare_parts", "alembic_version"} <= tables
