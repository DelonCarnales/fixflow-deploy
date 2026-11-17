# FixFlow Observability Stack

This stack adds OpenTelemetry traces, metrics and logs; Prometheus scraping and alert rules; Grafana dashboards; Alertmanager; and an AI on-call webhook responder.

## Start locally

From the repository root:

```bash
cp .env.example .env
# Optional: set OPENAI_API_KEY and SLACK_WEBHOOK_URL in .env
docker compose -f docker-compose.yml -f observability/docker-compose.yml up --build
```

Open:
- FixFlow: http://localhost:8000
- Grafana: http://localhost:3000 (user: admin; password: GRAFANA_PASSWORD, default is local-only)
- Prometheus: http://localhost:9090
- Alertmanager: http://localhost:9093
- OpenTelemetry Collector OTLP/HTTP: http://localhost:4318
- AI on-call health: http://localhost:9000/health

The application exposes Prometheus metrics at `/metrics`. OpenTelemetry SDKs export traces, metrics and logs to the Collector using OTLP/HTTP. The Collector currently writes received telemetry to its debug exporter so it is easy to demonstrate in Docker logs. Prometheus scrapes the application-specific metrics for dashboarding and alert rules.

## Application metrics

- `fixflow_http_requests_total{method,path,status}`: total requests, grouped by HTTP method, route and response status.
- `fixflow_http_request_duration_seconds_bucket`: request duration histogram, used for p95 latency.
- `fixflow_repair_orders_created_total`: number of repair orders created.
- `fixflow_repair_status_changes_total{from_status,to_status}`: repair workflow transitions.
- `fixflow_active_repair_orders`: current active repair-order count.
- `fixflow_low_stock_parts`: number of spare-part items at or below two units.
- OpenTelemetry instruments: `fixflow.http.requests` and `fixflow.http.request.duration`.

## Alerts

Prometheus evaluates:
- HTTP 5xx error ratio above 5% for two minutes.
- p95 response time above 1.5 seconds for two minutes.
- API target unavailable for one minute.
- At least one spare-part item at or below two units for one minute.

Alertmanager sends firing and resolved events to the on-call agent at `/alerts`. With `OPENAI_API_KEY` configured, the agent uses the OpenAI API to summarize the incident and recommend safe diagnostics. It enriches the alert payload with live Prometheus request-rate, 5xx error-rate and p95-latency query results. Without a key it returns deterministic rule-based triage and clearly reports that an AI model was not used. Optionally set `SLACK_WEBHOOK_URL` to deliver incident reports to Slack. The agent does not execute production changes.

## Demo an alert

Generate 5xx responses by requesting `http://localhost:8000/debug/500` repeatedly. This endpoint is enabled only by the local observability Compose overlay and is not present in Production. Alternatively, temporarily lower a threshold in `alerts.yml`. Wait for the configured `for` duration, then inspect Prometheus Alerts, Alertmanager, and the on-call agent logs:

```bash
docker compose -f docker-compose.yml -f observability/docker-compose.yml logs -f oncall-agent alertmanager
```

Restore any temporary threshold change after the demonstration.

## Stop

```bash
docker compose -f docker-compose.yml -f observability/docker-compose.yml down
```

Use `down -v` only if you intentionally want to delete Prometheus and Grafana history.
