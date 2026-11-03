# Instructions for Coding Agents

Keep this project at a normal student level. Use clear code and avoid unnecessary advanced patterns.

## Before starting
- Read `README.md`, `docs/plan.md`, and `docs/spec.md`.
- Follow `docs/process.md`; GitHub Issues are the canonical backlog.
- Read `docs/team/pm.md` to groom a task before implementation.
- Read `docs/team/software-engineer.md` when implementing a task.
- Read `docs/team/qa-engineer.md` before QA or closing an issue.
- Read `docs/design-system.md` for UI changes and `docs/testing-guidelines.md` for tests.

## Development rules
- Work on one issue at a time.
- Do not start implementing an issue before it has a clear Goal, Description, Acceptance criteria, Out of scope, and Constraints section.
- Use HTML, CSS, and JavaScript modules for the frontend unless the project plan changes.
- Keep mock data and mock operations in `frontend/src/services/mockService.js`.
- Use the API contract in `openapi.yaml`.
- Use FastAPI for endpoints and SQLAlchemy for database access.
- Do not add features outside the MVP without a good reason.
- Add or update tests when behavior changes.
- Do not claim that a test passed unless it was actually run.
- The engineer does not close issues. QA checks the running behavior and posts a PASS or FAIL comment first.
- If a bug is found while manually using the app, create an issue with the `user-test-bug` label. Include Goal, Description, reproduction steps, expected result, actual result, and environment. PM grooms it; QA adds and runs test cases.
- Keep the Markdown docs updated when project decisions change.
