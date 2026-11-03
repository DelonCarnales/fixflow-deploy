from e2e.helpers import create_order


def test_status_filter_and_search_can_be_combined(page, base_url):
    order = create_order(page, status="Diagnosing")
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    page.get_by_label("Filter by status").select_option(label="Diagnosing")
    assert page.get_by_text(order["id"], exact=True).is_visible()
    page.get_by_label("Search repair orders").fill(order["deviceModel"])
    assert page.get_by_text(order["id"], exact=True).is_visible()
    page.get_by_label("Search repair orders").fill("not-a-match")
    assert page.get_by_text(order["id"], exact=True).count() == 0


def test_each_status_can_be_selected(page, base_url):
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    select = page.get_by_label("Filter by status")
    for status in ["Received", "Diagnosing", "Waiting for parts", "Repairing", "Ready for pickup", "Completed", "Cancelled"]:
        select.select_option(label=status)
        assert select.input_value() == status
