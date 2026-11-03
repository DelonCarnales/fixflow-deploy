# AI Usage Report

## How AI was used
AI assistance was used to brainstorm the project idea, organize the specification, draft documentation, split work into GitHub Issues, and help implement and test the first version. The code and project scope are kept at a level that a student can understand and explain.

## Decisions made for FixFlow
- Chose a repair shop workflow instead of a generic tracker.
- Kept the MVP to repair orders, order search/filter, status history, spare parts, and customer status lookup.
- Chose HTML, CSS, and JavaScript modules for the first frontend so it stays easy to run and understand.
- Chose FastAPI for the backend.
- Chose OpenAPI as the contract between frontend and backend.
- Chose SQLite with SQLAlchemy for persistent storage.
- Worked in stages: mock frontend, API contract, in-memory backend, database storage, then frontend/backend integration.

## How generated work is checked
Generated code and docs are drafts, not proof of correctness. The project has automated tests in GitHub Actions. The browser smoke test uses Playwright to create and edit data through the app, with FastAPI and SQLite running. Bugs found while testing should be recorded as `user-test-bug` issues with PM/QA notes, and an issue should only be closed after its acceptance criteria are checked.

## Current status
The core frontend, OpenAPI contract, FastAPI backend, and SQLite ORM storage are in the repository. The frontend service now uses the API by default and supports mock mode for frontend-only work. The latest end-to-end integration test result is available in GitHub Actions.
