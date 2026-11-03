# Development Process

## GitHub issues are the backlog
GitHub Issues are the source of truth for tasks. `docs/github-issues-plan.md` is only an index; if it differs from GitHub, GitHub wins.

## Labels
- `mvp`: required for the first working version
- `post-mvp`: optional improvements after the MVP
- `user-test-bug`: bugs found while testing the running app

## Issue lifecycle
1. Pick an open issue.
2. PM grooms the issue using `docs/task-template.md` and `docs/team/pm.md`.
3. Engineer implements the issue and writes/updates tests; engineer does not close the issue.
4. QA uses `docs/team/qa-engineer.md`, runs tests, checks the app when possible, and posts a PASS or FAIL comment.
5. If QA finds a failure, the engineer fixes it and QA retests.
6. Close an issue only after QA posts PASS.
7. Repeat until every MVP issue and every `user-test-bug` issue is closed.

## Bug workflow
When a bug is discovered while using the running app:
- Create an issue with the `user-test-bug` label.
- Include Goal, Description, reproduction steps, expected result, actual result, and environment.
- PM grooms the issue and clarifies scope.
- QA adds test cases and checks the fix.
- The issue remains open until the fix is verified.

## Development stages
1. Plan and document the app.
2. Build the frontend with mockService.
3. Define the frontend/backend contract in `openapi.yaml`.
4. Implement FastAPI with an in-memory store.
5. Replace the in-memory store with SQLite and SQLAlchemy.
6. Connect the frontend service to the API.
7. Run the full app and test the main flows.

## Useful commands

The following server commands are for **local development on a Mac or PC**. In Codespaces, use port 8000 for the combined app as documented in the root README.

- Frontend tests: `cd frontend && npm test`
- Backend tests: `cd backend && python -m pytest -q`
- Local frontend server: `cd frontend && python3 -m http.server 5173`
- Local backend server: `cd backend && python -m uvicorn main:app --reload --port 8000`
