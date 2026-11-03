def test_dashboard_summary_cards(page, base_url):
    page.goto(base_url, wait_until="networkidle")

    page.get_by_role("heading", name="Good afternoon").wait_for()
    assert page.get_by_text("Active orders", exact=True).is_visible()
    assert page.get_by_text("Waiting for parts", exact=True).first.is_visible()
    assert page.get_by_text("Ready for pickup", exact=True).first.is_visible()
    assert page.get_by_text("Completed", exact=True).first.is_visible()
    assert page.get_by_text("Live backend", exact=True).is_visible()
