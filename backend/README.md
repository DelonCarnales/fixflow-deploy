# Backend

The backend uses FastAPI and SQLAlchemy. By default, data is saved in a local SQLite file called `fixflow.db`. Sample records are added the first time the app starts.

## Run locally

From the `backend` folder:

```bash
python3 -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```

Open http://127.0.0.1:8000/docs for the API page.

## GitHub Codespaces

In Codespaces, this FastAPI app also serves the frontend files from the repository's `frontend` folder. Open the forwarded port labelled **FixFlow App** (8000) to use the complete app. The frontend and API share one origin, avoiding cross-port browser access issues. See the root README for launch and restart instructions.

## Database

The default database URL is `sqlite:///./fixflow.db`. You can set `DATABASE_URL` before starting the server to use a different SQLAlchemy-supported database, as long as its driver is installed.

## Tests

From the `backend` folder:

```bash
python -m pytest -q
```

The API tests use a temporary SQLite database so test data does not change the local demo database.
