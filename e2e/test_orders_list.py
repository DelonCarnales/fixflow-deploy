def test_repair_orders_list_shows_orders_and_navigation(page, base_url):
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    page.get_by_role("heading", name="Repair orders").wait_for()
    assert page.get_by_role("textbox", name="Search repair orders").is_visible()
    assert page.get_by_text("FF-1001", exact=True).is_visible()
    assert page.get_by_text("FF-1002", exact=True).is_visible()
    assert page.get_by_text("MacBook Air M1", exact=True).is_visible()
