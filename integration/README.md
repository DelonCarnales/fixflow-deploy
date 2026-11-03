# Compose integration tests

Run against the live Docker Compose application and PostgreSQL service:

    docker compose up --build -d
    python -m pip install -r integration/requirements.txt
    TEST_DATABASE_URL=postgresql://fixflow:fixflow@localhost:5432/fixflow python -m pytest -q integration

The suite checks the HTTP health endpoint, static frontend assets, API-to-PostgreSQL persistence and Alembic schema tables.
