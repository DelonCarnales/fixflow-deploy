from e2e.helpers import create_order


def test_order_details_show_all_repair_information(page, base_url):
    order = create_order(page, technician="", notes="")
    page.goto(base_url, wait_until="networkidle")
    page.locator('[data-page="orders"]').click()
    page.locator(f'button.order-link[data-open="{order["id"]}"]').click()
    page.get_by_role("heading", name=order["deviceModel"]).wait_for()
    for value in [order["customerName"], order["phone"], "Laptop", order["deviceModel"], order["problem"], "Not assigned", "No notes added."]:
        assert page.get_by_text(value, exact=True).is_visible()
    assert page.get_by_text("12,500 ₸", exact=True).is_visible()
    assert page.get_by_text("Received", exact=True).first.is_visible()
    assert page.get_by_text(order["receivedDate"], exact=False).is_visible()
