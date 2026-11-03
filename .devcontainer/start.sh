#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Retire the previous split-port setup. The API now serves the frontend too,
# so browser requests stay on one origin and do not depend on cross-port CORS.
pkill -f '[u]vicorn main:app' >/dev/null 2>&1 || true
pkill -f '[p]ython3 -m http.server 5173 --bind 0.0.0.0' >/dev/null 2>&1 || true
sleep 1

nohup bash -c "cd '$ROOT_DIR/backend' && exec python -m uvicorn main:app --host 0.0.0.0 --port 8000" >/tmp/fixflow-backend.log 2>&1 &

for attempt in $(seq 1 30); do
  if curl --silent --fail http://127.0.0.1:8000/health >/dev/null 2>&1 \
    && curl --silent --fail http://127.0.0.1:8000/ | grep -q '<title>FixFlow - Repair Desk</title>'; then
    echo "FixFlow is running."
    echo "Frontend and API: port 8000"
    exit 0
  fi
  sleep 1
done

echo "FixFlow did not start correctly. Check /tmp/fixflow-backend.log."
exit 1
