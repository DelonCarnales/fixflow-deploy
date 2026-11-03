# FixFlow

FixFlow is a small web app for a computer and laptop repair shop. It keeps repair orders, customer details, repair status, and spare parts in one place.

This is a student project for a Web Frontend course. The goal is to build a working app step by step and keep the code easy to understand.

## Main features
- View, search, and filter repair orders
- Add and edit repair orders
- Change repair status and view its history
- Add and edit spare parts
- Let customers check a repair status by order number

## Stack
- Frontend: HTML, CSS, and JavaScript modules
- Backend: Python and FastAPI
- API contract: OpenAPI in `openapi.yaml`
- Database: SQLite with SQLAlchemy ORM
- Tests: Node's built-in test runner, Pytest, and Playwright browser checks

## Run locally on a Mac or PC

For local development, run the backend and frontend in separate terminals.

Terminal 1 — backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Terminal 2 — frontend (from the repository root):

```bash
cd frontend
python3 -m http.server 5173
```

Open http://localhost:5173. In this local setup, the frontend calls the API at http://127.0.0.1:8000. To use sample data without the backend, open http://localhost:5173/?mock=1.

The API docs are at http://127.0.0.1:8000/docs. The default SQLite database file is created in the backend folder.

## Run in GitHub Codespaces (no local installation)

Codespaces uses a different setup from local development: **FastAPI serves both the frontend and API on port 8000**, so the page and API share one origin. Port 5173 is not used by the Codespaces startup script.

1. Open the repository on GitHub.
2. Click the green **Code** button and select **Codespaces**.
3. Click **Create codespace on main**.
4. Wait for the environment setup to finish.
5. Open the forwarded port labelled **FixFlow App** (8000). If it did not open automatically, use the **Ports** tab and choose **Open in Browser** for port 8000.

To update an existing Codespace and restart the app, run these commands in its terminal:

```bash
git pull
bash .devcontainer/start.sh
```

If Git reports local changes or a merge conflict, stop and review the message rather than resetting files. The Codespaces configuration forwards only port 8000. The port is private by default; do not make it public when using real customer data. This project uses fictional demo records.

## Run tests

Frontend mock service tests:

```bash
cd frontend
npm test
```

Backend API and OpenAPI tests:

```bash
cd backend
python -m pip install -r requirements.txt
python -m pytest -q
```

Browser smoke tests use Playwright and open the frontend served by FastAPI on port 8000. Start the backend from the local setup above first; the separate frontend server on port 5173 is not needed for this test. Then, from the repository root in another terminal, run:

```bash
python -m pip install -r frontend/requirements-test.txt
python -m playwright install chromium
python frontend/tests/browser_smoke.py
```

GitHub Actions checks JavaScript syntax, mock service tests, browser flows against FastAPI and SQLite, backend/OpenAPI tests, and the Codespaces startup configuration. See the [latest workflow run](https://github.com/DelonCarnales/fixflow/actions) for the actual result.

## Development stages
1. Plan and write the docs.
2. Build the frontend using mock data.
3. Define the API in OpenAPI.
4. Build the backend with temporary in-memory data.
5. Replace the temporary store with SQLite using SQLAlchemy.
6. Connect the frontend to the backend.
7. Run the complete app and test the main flows.

## Current status
The repository contains project planning docs, the frontend, a mock service, an OpenAPI contract, and a FastAPI backend with SQLite/SQLAlchemy persistence. The frontend uses the real API by default and supports mock mode with `?mock=1`. Codespaces runs the interface and API together on port 8000; local development uses frontend port 5173 and backend port 8000.
