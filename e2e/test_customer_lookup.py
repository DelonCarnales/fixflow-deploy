from e2e.helpers import create_order


def test_customer_lookup_is_case_insensitive_and_private(page, base_url):
    order = create_order(page, status="Ready for pickup", technician="Secret technician", notes="Secret staff notes")
    page.goto(base_url, wait_until="networkidle")
    page.locator('[data-page="lookup"]').click()
    field = page.locator("#lookup-number")
    field.fill(order["id"].lower())
    page.get_by_role("button", name="Check status").click()
    result = page.locator("#lookup-result")
    result.get_by_text(order["deviceModel"], exact=True).wait_for()
    assert result.get_by_text("Ready for pickup", exact=True).is_visible()
    assert result.get_by_text("Your device is ready. Please contact the shop to arrange pickup.", exact=True).is_visible()
    assert result.get_by_text(order["receivedDate"], exact=False).is_visible()
    assert "Secret technician" not in result.inner_text()
    assert "Secret staff notes" not in result.inner_text()
    field.fill("FF-9999")
    page.get_by_role("button", name="Check status").click()
    page.get_by_role("alert").get_by_text("We could not find order FF-9999", exact=False).wait_for()
