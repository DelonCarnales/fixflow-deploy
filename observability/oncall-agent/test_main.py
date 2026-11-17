import main
from fastapi.testclient import TestClient


def test_alertmanager_webhook_returns_safe_triage_without_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setattr(main, "fetch_prometheus_context", lambda: {"request_rate_per_second": []})
    client = TestClient(main.app)
    response = client.post("/alerts", json={
        "status": "firing",
        "alerts": [{
            "labels": {"alertname": "FixFlowHighErrorRate", "severity": "warning"},
            "annotations": {"description": "The 5xx ratio is above the configured threshold."}
        }]
    })
    assert response.status_code == 200
    body = response.json()
    assert body["received"] is True
    assert body["ai_used"] is False
    assert "FixFlowHighErrorRate" in body["alerts"]
    assert "database connectivity" in body["analysis"]
