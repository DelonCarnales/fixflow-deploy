def test_backend_error_message_keeps_navigation_available(page, base_url):
    page.route("**/orders", lambda route: route.abort())
    page.route("**/parts", lambda route: route.abort())
    page.goto(base_url, wait_until="domcontentloaded")
    page.get_by_text("Could not connect to the backend", exact=False).wait_for()
    page.get_by_role("button", name="Spare parts").click()
    assert page.get_by_role("heading", name="Spare parts").is_visible()
