from datetime import date
from uuid import uuid4


def unique_name(prefix="E2E"):
    return f"{prefix}-{uuid4().hex[:8]}"


def create_order(page, *, customer=None, model=None, status="Received", technician="E2E tech", notes="E2E notes"):
    customer = customer or unique_name("Customer")
    model = model or unique_name("Device")
    response = page.request.post("/orders", data={
        "customerName": customer,
        "phone": "+7 700 000 00 00",
        "deviceType": "Laptop",
        "deviceModel": model,
        "problem": "E2E test problem",
        "receivedDate": date.today().isoformat(),
        "status": status,
        "technician": technician,
        "estimatedCost": 12500,
        "notes": notes,
    })
    assert response.status == 201, response.text()
    return response.json()


def create_part(page, *, name=None, stock=5, unit_price=2500):
    name = name or unique_name("Part")
    response = page.request.post("/parts", data={"name": name, "stock": stock, "unitPrice": unit_price})
    assert response.status == 201, response.text()
    return response.json()


def open_order(page, order):
    page.goto(page.url.split("/", 3)[0] + "//" + page.url.split("/", 3)[2], wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    page.locator(f'[data-open="{order["id"]}"]').click()
    page.get_by_role("heading", name=order["deviceModel"]).wait_for()
