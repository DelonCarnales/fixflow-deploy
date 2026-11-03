# FixFlow - one image that serves the static frontend and the FastAPI backend.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Run the app as a normal user instead of root.
RUN useradd --create-home --uid 10001 fixflow

WORKDIR /app

# Install the Python packages first so Docker can cache this layer.
COPY backend/requirements-prod.txt backend/requirements-prod.txt
RUN pip install --no-cache-dir -r backend/requirements-prod.txt

# The frontend is plain HTML, CSS and JavaScript, so it is copied as static files.
# FastAPI serves the "frontend" folder that sits next to "backend" (see backend/main.py).
COPY frontend frontend
COPY backend backend

RUN chown -R fixflow:fixflow /app
USER fixflow

WORKDIR /app/backend
EXPOSE 8000

# DATABASE_URL tells the app which database to use (SQLite by default).
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"

# entrypoint.sh runs the database migrations and then starts the server.
CMD ["sh", "entrypoint.sh"]
