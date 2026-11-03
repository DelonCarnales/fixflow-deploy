# GitHub Issues Index

GitHub Issues are the canonical backlog. This document is only a quick index; GitHub issue state, labels, and comments take precedence if anything differs.

## MVP issues
- #1 Set up the frontend project — closed (QA PASS)
- #2 Finalize MVP scope and acceptance criteria — closed (QA PASS)
- #3 Set up basic app layout and sidebar — closed (QA PASS)
- #4 Add dashboard with mock data — closed (QA PASS)
- #5 Add repair orders table — closed (QA PASS)
- #6 Add order search and status filter — closed (QA PASS)
- #7 Add create repair order form — closed (QA PASS)
- #8 Add repair order form validation — closed (QA PASS)
- #9 Add repair order details page — closed (QA PASS)
- #10 Add status updates and repair history — closed (QA PASS)
- #11 Add edit repair order form — closed (QA PASS)
- #12 Add spare parts page — closed (QA PASS)
- #13 Add customer order status lookup page — closed (QA PASS)
- #14 Create OpenAPI contract — closed (QA PASS)
- #15 Set up FastAPI backend — closed (QA PASS)
- #16 Implement in-memory repair order endpoints — closed (QA PASS)
- #17 Implement in-memory spare parts endpoints — closed (QA PASS)
- #18 Add SQLAlchemy models — closed (QA PASS)
- #19 Replace in-memory store with SQLite — closed (QA PASS)
- #20 Connect frontend service to the real API — closed (QA PASS)
- #21 Add frontend tests — closed (QA PASS)
- #22 Add backend API tests — closed (QA PASS)
- #23 Run full repair workflow in a browser — closed (QA PASS)
- #24 Update README with setup and testing commands — closed (QA PASS)
- #28 Create one mockService for frontend data — closed (QA PASS)

## Post-MVP issues
- #25 Improve mobile layout — open
- #26 Add sorting to repair orders table — open
- #27 Add CSV export for repair orders — open

## Bugs found while testing
- #29 Fix spare-part ID generation syntax — closed (QA PASS)
- #30 Treat the expected unknown-order 404 as handled — closed (QA PASS)

## Latest verified checks

[GitHub Actions run #59](https://github.com/DelonCarnales/fixflow/actions/runs/39838767625) passed on October 22, 2026:
- 8 frontend mock service tests
- 14 browser smoke checks against the frontend, FastAPI, and SQLite
- 16 backend/API/OpenAPI/CORS tests (with 3 non-failing warnings)
- Codespaces devcontainer JSON and startup script syntax checks
- Browser checks open the app through FastAPI on port 8000, matching the single-port Codespaces setup; the CI job no longer starts a separate port 5173 frontend server

## Workflow
Every issue should have Goal, Description, Acceptance criteria, Out of scope, and Constraints. PM grooms the scope. The engineer implements without closing it. QA checks acceptance criteria, runs tests, posts a PASS/FAIL comment, and closes only after PASS.
