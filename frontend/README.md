# Frontend

The frontend uses plain HTML, CSS, and JavaScript modules. It has no third-party frontend dependencies.

## Run locally with the backend

These instructions are for running on your own Mac or PC. First start the FastAPI backend as described in `../backend/README.md`. Then, from the repository's `frontend` folder, run:

```bash
python3 -m http.server 5173
```

Open http://localhost:5173. In this local setup, the frontend calls the backend at http://127.0.0.1:8000.

## Run in GitHub Codespaces

In Codespaces, do **not** use the separate-port instructions above. The FastAPI server serves both the frontend and API on port 8000, so the app uses one origin.

1. Open the repository and select **Code → Codespaces → Create codespace on main**.
2. Wait for the environment setup to finish.
3. Open the forwarded port labelled **FixFlow App** (8000). If it did not open, use the **Ports** tab and choose **Open in Browser** for port 8000.

For an existing Codespace with an older server still running, run `git pull` and then `bash .devcontainer/start.sh` in its terminal. See the root README for details.

## Run with mock data

For local development, open http://localhost:5173/?mock=1. This loads `src/services/mockService.js` without calling the backend. The data is held in memory and resets when the page reloads.

## Tests

Run the mock service tests from this folder:

```bash
npm test
```

The Playwright browser tests exercise the main pages against the SQLite-backed API. See `tests/browser_smoke.py`.
