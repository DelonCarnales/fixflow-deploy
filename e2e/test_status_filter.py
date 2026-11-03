from e2e.helpers import create_order


def test_status_filter_and_search_can_be_combined_and_cleared(page, base_url):
    diagnosing = create_order(page, status="Diagnosing")
    received = create_order(page, status="Received")
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    select = page.get_by_label("Filter by status")
    select.select_option(label="Diagnosing")
    assert page.get_by_text(diagnosing["id"], exact=True).is_visible()
    assert page.get_by_text(received["id"], exact=True).count() == 0
    for row in page.locator("tr.clickable-row").all():
        assert row.locator("td").nth(4).inner_text() == "Diagnosing"
    page.get_by_label("Search repair orders").fill(diagnosing["deviceModel"])
    assert page.get_by_text(diagnosing["id"], exact=True).is_visible()
    page.get_by_label("Search repair orders").fill("not-a-match")
    assert page.get_by_text("No repair orders match your search.", exact=True).is_visible()
    select.select_option(label="All statuses")
    assert page.locator("tr.clickable-row").count() == len(page.request.get(base_url + "/orders").json())


def test_each_of_seven_statuses_can_be_selected(page, base_url):
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    select = page.get_by_label("Filter by status")
    for status in ["Received", "Diagnosing", "Waiting for parts", "Repairing", "Ready for pickup", "Completed", "Cancelled"]:
        select.select_option(label=status)
        assert select.input_value() == status
