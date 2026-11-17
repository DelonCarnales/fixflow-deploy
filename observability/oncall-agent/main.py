"""Alertmanager webhook receiver and AI incident triage assistant."""
import json
import logging
import os
from typing import Any
from urllib.request import Request, urlopen
from urllib.parse import urlencode

from fastapi import FastAPI, HTTPException, Request as FastAPIRequest

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("fixflow.oncall")
app = FastAPI(title="FixFlow AI On-call Agent", version="1.0.0")


def fallback_analysis(payload: dict[str, Any]) -> str:
    alerts = payload.get("alerts", [])
    if not alerts:
        return "No active alert details were supplied. Check Alertmanager payload and Prometheus targets."
    lines = []
    for alert in alerts:
        name = alert.get("labels", {}).get("alertname", "Unknown alert")
        description = alert.get("annotations", {}).get("description", "No description supplied.")
        if name == "FixFlowHighErrorRate":
            advice = "Inspect recent backend logs and traces; check database connectivity and recent deployments."
        elif name == "FixFlowSlowResponses":
            advice = "Inspect p95 traces, database query duration, and resource saturation."
        elif name == "FixFlowApiDown":
            advice = "Check container health, application logs, database availability, and the /health endpoint."
        else:
            advice = "Inspect the related Prometheus series, application logs, and traces before taking action."
        lines.append(f"{name}: {description}\nRecommended checks: {advice}")
    return "\n\n".join(lines)


def fetch_prometheus_context() -> dict[str, Any]:
    base = os.getenv("PROMETHEUS_URL", "http://prometheus:9090").rstrip("/")
    queries = {
        "request_rate_per_second": "sum(rate(fixflow_http_requests_total[5m]))",
        "server_error_rate": "sum(rate(fixflow_http_requests_total{status=~\"5..\"}[5m])) / clamp_min(sum(rate(fixflow_http_requests_total[5m])), 0.001)",
        "p95_response_seconds": "histogram_quantile(0.95, sum(rate(fixflow_http_request_duration_seconds_bucket[5m])) by (le))",
    }
    snapshot: dict[str, Any] = {}
    for name, query in queries.items():
        try:
            url = f"{base}/api/v1/query?{urlencode({'query': query})}"
            with urlopen(url, timeout=3) as response:
                result = json.loads(response.read().decode("utf-8"))
            snapshot[name] = result.get("data", {}).get("result", [])
        except Exception as exc:
            snapshot[name] = {"unavailable": str(exc)}
    return snapshot


def analyze_with_ai(payload: dict[str, Any]) -> tuple[str, bool]:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        return fallback_analysis(payload), False
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            instructions=(
                "You are FixFlow's on-call SRE assistant. Analyze Alertmanager incidents. "
                "Summarize severity, likely causes, evidence, and safe diagnostic steps. "
                "Never claim to have inspected logs or traces that are not in the payload. "
                "Do not execute actions, change production, or request secrets. "
                "Clearly distinguish evidence from hypotheses."
            ),
            input=json.dumps(payload, ensure_ascii=False)[:18000],
        )
        return response.output_text, True
    except Exception:
        logger.exception("AI analysis failed; using local triage")
        return fallback_analysis(payload), False


def send_slack_message(text: str) -> None:
    webhook = os.getenv("SLACK_WEBHOOK_URL", "")
    if not webhook:
        return
    request = Request(webhook, data=json.dumps({"text": text}).encode("utf-8"),
                      headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=8) as response:
        response.read()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/alerts")
async def receive_alert(request: FastAPIRequest) -> dict[str, Any]:
    try:
        payload = await request.json()
    except Exception as exc:
        raise HTTPException(status_code=400, detail="Expected an Alertmanager JSON payload") from exc
    payload['telemetry_context'] = fetch_prometheus_context()
    analysis, ai_used = analyze_with_ai(payload)
    status = payload.get("status", "unknown")
    alert_names = [a.get("labels", {}).get("alertname", "Unknown") for a in payload.get("alerts", [])]
    report = (f"FixFlow on-call incident ({status})\nAlerts: {', '.join(alert_names) or 'none'}\n"
              f"AI model used: {'yes' if ai_used else 'no — configure OPENAI_API_KEY'}\n\n{analysis}")
    logger.warning("%s", report)
    try:
        send_slack_message(report)
    except Exception:
        logger.exception("Could not deliver incident report to Slack")
    return {"received": True, "ai_used": ai_used, "alerts": alert_names, "analysis": analysis}


@app.get("/")
def root() -> dict[str, str]:
    return {"service": "FixFlow AI On-call Agent", "health": "/health", "webhook": "/alerts"}
