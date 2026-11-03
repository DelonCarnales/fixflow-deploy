# Project Plan

## Idea
FixFlow is a simple repair-order management app for a small laptop and computer repair shop.

## Why I picked it
I wanted an idea that is more useful than a basic list app, but still possible to finish for a university project. A repair shop has a clear workflow: customers bring devices in, staff record the problem, update repair status, and track simple spare parts.

## Main users
- Shop employee: creates orders and updates their status.
- Technician: checks repair details and adds notes.
- Customer: checks the current status using an order number.

## Development stages
1. **Planning:** project docs, design references, GitHub labels, and issues.
2. **Frontend with mockService:** build pages and interactions with local mock data.
3. **OpenAPI contract:** describe the API in `openapi.yaml`.
4. **Backend in memory:** implement API endpoints with temporary data.
5. **SQLite:** replace the in-memory store with SQLAlchemy and persistent storage.
6. **Integration:** use the real API by default while keeping `?mock=1` for frontend-only work.
7. **Testing:** run service tests, backend tests, browser checks, and fix issues found during testing.

## MVP checklist
- [x] Dashboard with basic counts
- [x] Repair orders list
- [x] Search and status filter
- [x] Create and edit repair order
- [x] Repair details page
- [x] Change repair status and view history
- [x] Customer and device details
- [x] Simple spare-parts list
- [x] Public order status lookup
- [x] OpenAPI contract
- [x] FastAPI backend
- [x] SQLAlchemy models and SQLite storage
- [x] Frontend connected to the real API
- [x] Mock mode remains available for frontend-only work
- [x] Service, backend, and contract tests
- [x] Browser test for the main repair workflow
- [x] Refresh persistence and database-file restart test
- [x] Connection-error state check

## Not in MVP
- Online payments
- SMS or email notifications
- AI diagnosis
- Multi-branch shop support
- Complex staff roles and permissions

## Definition of done
A feature is done when the acceptance criteria are checked, relevant tests are actually run, the running app is tested when possible, and QA posts a PASS comment before the issue is closed.
