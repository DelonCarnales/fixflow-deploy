# Testing Guidelines

## Frontend service tests
Run from the `frontend` folder with `npm test`. This uses Node's built-in test runner, so there is no install step.

- The mock service returns seeded orders.
- Creating an order gives it a new order number and initial history.
- Editing an order updates its fields and only adds a history entry when its status changes.
- Changing status updates the order and appends a history entry.
- Negative spare-part quantity and price are rejected.
- Adding a spare part creates a new ID.

## Full browser test
The Playwright test at `frontend/tests/browser_smoke.py` opens the app from FastAPI at `http://127.0.0.1:8000`. This deliberately tests the same-origin setup used by Codespaces, where FastAPI serves both the frontend and API. The local split-port setup (frontend 5173, API 8000) is still available for local development.

- Dashboard and recent orders load from the API.
- Search and status filters work.
- Required form fields show validation errors.
- A new order can be created and edited.
- The edited order remains visible after a browser refresh.
- A status change is shown with history.
- Spare parts can be added and renamed without changing their IDs.
- Customer lookup handles a known and an unknown order number.
- The browser has no unexpected console errors (the deliberate unknown-order 404 is expected).
- The page has no page-level horizontal overflow at a phone-sized viewport.
- If the backend is unavailable, the UI shows a readable connection error.

The GitHub Actions workflow starts FastAPI with a fresh SQLite file and runs the browser test from the FastAPI-served frontend. This checks that the interface, static assets, and API requests work on one origin, as configured for Codespaces. See the linked Actions run for the actual result.

## Backend tests
The Pytest tests use a temporary SQLite database. They cover:
- Health endpoint and listing orders
- Creating orders and status history
- Rejecting blank required fields and negative costs
- Editing an order and recording status changes
- Returning 404 for unknown IDs
- Creating and updating spare parts
- Rejecting negative stock
- Excluding private notes and phone from the customer lookup response
- Combining order search and status filters
- Reading saved order data in a later request
- Required OpenAPI paths and schemas

## Bug reporting
For a bug found while manually using the running app, create a GitHub issue with:
- Label: `user-test-bug`
- Goal
- Description
- Steps to reproduce
- Expected result
- Actual result
- Browser/OS if relevant

Do not write that a test passed unless it was actually run.
