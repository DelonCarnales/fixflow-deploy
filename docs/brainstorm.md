# Brainstorming and Chat History

This file records the user-visible discussion that happened before implementation started. It is a short transcript of the relevant conversation, not platform metadata.

## 1. Assignment request

**Student:**

> Pick a project idea, different from Part I, and come up with a non trivial app (no habit tracker, to-do list, etc). Come up with an idea you will be proud to show off.
>
> Fully follow the AI-native development and full-stack app articles. Use GitHub Issues, a design agent or good design references, close all MVP tags, use SQLite and an ORM, and work in iterations: frontend with mockService, OpenAPI contract, backend with in-memory data, SQLite storage, then frontend/backend integration.
>
> Add the Markdown files and brainstorming chat history to the repo. Actually run the app and thoroughly test it. When testing finds a bug, create a GitHub issue with Goal and Description, have PM groom it and QA add test cases. Use the labels `mvp`, `post-mvp`, and `user-test-bug`.

## 2. Initial project proposal

**Assistant:**

> I proposed FixFlow, a repair-order management app for a small computer and laptop repair shop. It would let staff create repair orders, track repair status and history, manage a simple spare-parts list, and let customers check order status by number.

The idea was selected because it has a real workflow but is small enough for a university project.

## 3. Student preference

**Student:**

> не надо делать прям вау, сделай попроще используй обычные вещи не то что знают мидл или сениор а как обычный студент. если только по рекомендациям в задании не просят того. начни делать этап 1. 1)создай сам репозитории 2)хз 3)англ

**Assistant:**

> I kept the project at a normal student level, with English documentation and a simple interface. The first docs included a plan, specification, design notes, testing rules, architecture notes, role files for PM/engineer/QA, a task template, and GitHub issue templates.

## 4. Repository setup

**Assistant:**

> I explained that the GitHub connector needed to be connected before I could publish the files or create Issues.

**Student:**

> https://github.com/DelonCarnales/fixflow

After the student created the public repository, the project documents and GitHub issues were added there.

## 5. Decisions made before and during the first implementation

- Use plain HTML, CSS, and JavaScript modules for the frontend so it is easy to run and explain.
- Use a simple dashboard, tables, forms, status labels, and a sidebar, following the dashboard layout references in `docs/design-system.md`.
- Use a single mock service for frontend-only work.
- Define the API in `openapi.yaml`.
- Use FastAPI for the API.
- Use SQLAlchemy ORM with SQLite by default and read the database URL from `DATABASE_URL`.
- Keep `?mock=1` available so the frontend can still be used without the backend.
- Use GitHub Issues as the canonical backlog and keep the app features limited to the MVP.

## 6. Implementation stages

1. Plan the app and write the docs.
2. Build the frontend with mockService.
3. Add the OpenAPI contract.
4. Implement the backend with temporary in-memory data.
5. Replace the temporary store with SQLite and SQLAlchemy.
6. Connect the frontend service to the backend.
7. Run browser tests and backend tests; create and fix issues for problems found during real testing.

## Current status when this note was updated

The frontend, OpenAPI contract, FastAPI backend, SQLite persistence, integration service, and browser smoke tests are in the repository. The exact current test status is linked from GitHub Actions and the relevant GitHub Issues.
