# FixFlow

FixFlow is a repair-shop management app for repair orders, customer status lookup and spare-parts inventory.

## Stack
- Frontend: static HTML, CSS and JavaScript modules
- Backend: Python 3.12, FastAPI and SQLAlchemy
- Database: PostgreSQL 16 in Docker Compose; SQLite remains available for local development and backend unit tests
- Migrations: Alembic
- Tests: Node unit tests, Pytest backend/integration tests and Python Playwright E2E tests
- Deployment: Dockerfile, Docker Compose, Render Blueprint, Railway Dockerfile configuration and optional Vercel static frontend

## Run the complete application

    cp .env.example .env
    # Change POSTGRES_PASSWORD in .env before using anything beyond local demo data.
    docker compose up --build

Open http://localhost:8000. API docs are at http://localhost:8000/docs. PostgreSQL data is stored in the named fixflow-db volume. docker compose down preserves it; docker compose down -v deletes it.

## Local development with SQLite

    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.txt
    DATABASE_URL=sqlite:///./fixflow.db python -m uvicorn main:app --reload --port 8000

The frontend can be served separately from frontend/ on port 5173. In this split-port setup, its API service calls the backend on port 8000. FastAPI serves the static frontend automatically in the Docker image.

## Migrate an existing SQLite database

Start PostgreSQL, then run the schema migration and data-copy script:

    cd backend
    DATABASE_URL='postgresql://fixflow:YOUR_PASSWORD@localhost:5432/fixflow' alembic upgrade head
    cd ..
    python scripts/migrate_sqlite_to_postgres.py --source sqlite:///backend/fixflow.db --target 'postgresql://fixflow:YOUR_PASSWORD@localhost:5432/fixflow'

The script preserves primary keys and status-history ordering and skips rows already present, so rerunning it does not duplicate rows.

## Tests

Frontend unit tests:

    cd frontend && npm test

Backend tests (SQLite):

    python -m pip install -r backend/requirements.txt
    cd backend && python -m pytest -q

Compose integration and Playwright E2E tests (requires Docker):

    python -m pip install -r integration/requirements.txt -r e2e/requirements.txt
    python -m playwright install chromium
    docker compose up --build -d
    python -m pytest -q integration
    E2E_BASE_URL=http://localhost:8000 python -m pytest -q e2e
    # Run a second time to check repeatability against the same database.
    E2E_BASE_URL=http://localhost:8000 python -m pytest -q e2e

E2E tests use unique test records and run serially because order numbers are generated sequentially. Failed browser tests save screenshots and Playwright traces under test-results/.

## CI and deployment

GitHub Actions checks frontend, backend, Docker build, Compose integration and Playwright E2E tests on pull requests and pushes to main. See the Actions tab for actual run results. Deployment options and cost warnings are in deploy/README.md.

Cloud deployment is not performed automatically until the account owner supplies provider credentials and explicitly reviews billing. Do not enable paid AWS account features or deploy resources outside the account's free allowance.
