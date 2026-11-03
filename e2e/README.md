# End-to-end tests

These tests use Python Playwright and run against the real application started by Docker Compose.

```bash
python -m pip install -r e2e/requirements.txt
python -m playwright install --with-deps chromium
docker compose up --build -d
E2E_BASE_URL=http://localhost:8000 python -m pytest -q e2e
```

`E2E_BASE_URL` defaults to `http://localhost:8000`. Tests should create their own data through the app/API and must not depend on fixed generated order or part IDs. Run tests serially because order numbers are generated sequentially.
