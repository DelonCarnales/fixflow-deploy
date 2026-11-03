from datetime import date
from e2e.helpers import unique_name


def test_create_order_through_form(page, base_url):
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="New repair order").click()
    dialog = page.get_by_role("dialog", name="New repair order")
    assert dialog.locator('input[name="receivedDate"]').input_value() == date.today().isoformat()
    assert dialog.locator('select[name="status"]').input_value() == "Received"
    customer, model = unique_name("CreateCustomer"), unique_name("CreateDevice")
    dialog.locator('input[name="customerName"]').fill(customer)
    dialog.locator('input[name="phone"]').fill("+7 700 111 22 33")
    dialog.locator('input[name="deviceModel"]').fill(model)
    dialog.locator('textarea[name="problem"]').fill("Screen does not turn on")
    dialog.get_by_role("button", name="Create order").click()
    page.get_by_role("heading", name=model).wait_for()
    order_id = page.locator(".eyebrow").filter(has_text="REPAIR ORDER").inner_text().split("·")[-1].strip()
    assert order_id.startswith("FF-")
    assert page.get_by_text(customer, exact=True).is_visible()
    assert page.get_by_text("Received", exact=True).first.is_visible()
    assert page.locator(".history-item").count() == 1
    page.get_by_role("button", name="Repair orders").click()
    assert page.get_by_text(order_id, exact=True).is_visible()
