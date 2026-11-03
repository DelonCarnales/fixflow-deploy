def test_repair_orders_list_columns_footer_and_navigation(page, base_url):
    page.goto(base_url, wait_until="networkidle")
    orders = page.request.get(base_url + "/orders").json()
    page.locator('[data-page="orders"]').click()
    page.get_by_role("heading", name="Repair orders").wait_for()
    headers = [value.strip().lower() for value in page.locator("table thead th").all_inner_texts()]
    assert headers == ["order", "customer", "device", "received", "status", "technician"]
    assert page.get_by_text(f"Showing {len(orders)} of {len(orders)} orders", exact=True).is_visible()
    first_row = page.locator("tr.clickable-row").first
    order_id = first_row.locator("button.order-link").inner_text()
    device = first_row.locator("td").nth(2).locator("strong").inner_text()
    first_row.locator("button.order-link").click()
    page.get_by_role("heading", name=device).wait_for()
    page.get_by_role("button", name="Back to repair orders").click()
    assert page.get_by_role("heading", name="Repair orders").is_visible()
    assert page.get_by_text(order_id, exact=True).is_visible()
