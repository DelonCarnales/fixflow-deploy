#!/bin/sh
# Start script used by the Docker image: create or update the tables, then run the server.
set -e

alembic upgrade head
exec python -m uvicorn main:app --host 0.0.0.0 --port 8000
