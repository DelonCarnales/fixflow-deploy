import yaml
from pathlib import Path


def test_openapi_contract_has_frontend_routes_and_schemas():
    project_root = Path(__file__).resolve().parents[2]
    contract_path = project_root / "openapi.yaml"
    contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))

    assert contract["openapi"].startswith("3.")
    assert "/orders" in contract["paths"]
    assert "/orders/{orderId}" in contract["paths"]
    assert "/orders/{orderId}/status" in contract["paths"]
    assert "/parts" in contract["paths"]
    assert "/public/orders/{orderId}" in contract["paths"]
    assert "RepairOrder" in contract["components"]["schemas"]
    assert "SparePart" in contract["components"]["schemas"]
    assert "PublicOrderStatus" in contract["components"]["schemas"]
