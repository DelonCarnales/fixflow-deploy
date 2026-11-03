import os
import time

import httpx
import psycopg2

BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:8000").rstrip("/")
DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql://fixflow:fixflow@localhost:5432/fixflow",
)


def wait_for_app():
    last_error = None
    for _ in range(60):
        try:
            response = httpx.get(f"{BASE_URL}/health", timeout=3)
            if response.status_code == 200:
                return
        except httpx.HTTPError as exc:
            last_error = exc
        time.sleep(2)
    raise AssertionError(f"Application did not become healthy: {last_error}")


def test_compose_serves_frontend_and_health():
    wait_for_app()
    for path in ("/", "/styles.css", "/src/app.js"):
        response = httpx.get(f"{BASE_URL}{path}", timeout=10)
        assert response.status_code == 200, path
    assert httpx.get(f"{BASE_URL}/health").json() == {"status": "ok"}


def test_compose_database_has_migrated_tables():
    wait_for_app()
    with psycopg2.connect(DATABASE_URL) as connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            tables = {row[0] for row in cursor.fetchall()}
    assert {"customers", "devices", "repair_orders", "status_history", "spare_parts", "alembic_version"} <= tables
