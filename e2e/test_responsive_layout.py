from e2e.helpers import create_order


def test_all_main_pages_fit_mobile_viewport(page, base_url):
    order = create_order(page)
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(base_url, wait_until="networkidle")
    pages = ["Dashboard", "Repair orders", "Spare parts", "Customer lookup"]
    for name in pages:
        page.locator({"Dashboard": '[data-page="dashboard"]', "Repair orders": '[data-page="orders"]', "Spare parts": '[data-page="parts"]', "Customer lookup": '[data-page="lookup"]'}[name]).click()
        page.wait_for_timeout(100)
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), f"horizontal overflow on {name}"
        assert page.get_by_role("navigation", name="Main navigation").is_visible()
    page.locator('[data-page="orders"]').click()
    page.locator(f'button.order-link[data-open="{order["id"]}"]').click()
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth"), "horizontal overflow on order details"
