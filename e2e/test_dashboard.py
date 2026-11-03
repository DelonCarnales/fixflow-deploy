def test_dashboard_summary_cards_and_navigation(page, base_url):
    page.goto(base_url, wait_until="networkidle")
    orders = page.request.get(base_url + "/orders").json()
    assert page.get_by_role("heading", name="Good afternoon").is_visible()
    assert page.get_by_text("Live backend", exact=True).is_visible()
    expected = {
        "Active orders": sum(order["status"] not in ["Completed", "Cancelled"] for order in orders),
        "Waiting for parts": sum(order["status"] == "Waiting for parts" for order in orders),
        "Ready for pickup": sum(order["status"] == "Ready for pickup" for order in orders),
        "Completed": sum(order["status"] == "Completed" for order in orders),
    }
    for label, count in expected.items():
        card = page.locator(".stat-card").filter(has_text=label)
        assert card.locator(".stat-value").inner_text() == str(count)
    recent = page.locator(".content-card").filter(has_text="Recent repair orders")
    assert recent.locator("tr.clickable-row").count() <= 4
    overview = page.locator(".content-card").filter(has_text="Repair status overview")
    assert overview.locator(".status-bar-row").count() == 5
    for status in ["Received", "Diagnosing", "Waiting for parts", "Repairing", "Ready for pickup"]:
        assert overview.get_by_text(status, exact=True).is_visible()
    page.get_by_role("button", name="View all orders").click()
    assert page.get_by_role("heading", name="Repair orders").is_visible()
