def test_dashboard_summary_cards_match_live_api_counts(page, base_url):
    page.goto(base_url, wait_until="networkidle")
    orders = page.request.get(base_url + "/orders").json()
    expected = {
        "Active orders": sum(order["status"] not in ["Completed", "Cancelled"] for order in orders),
        "Waiting for parts": sum(order["status"] == "Waiting for parts" for order in orders),
        "Ready for pickup": sum(order["status"] == "Ready for pickup" for order in orders),
        "Completed": sum(order["status"] == "Completed" for order in orders),
    }
    for label, count in expected.items():
        card = page.locator(".stat-card").filter(has_text=label)
        assert card.locator(".stat-value").inner_text() == str(count)
    assert page.get_by_text("Live backend", exact=True).is_visible()
