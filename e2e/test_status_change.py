from e2e.helpers import create_order


def test_status_change_updates_badge_history_and_dashboard(page, base_url):
    order = create_order(page, status="Received")
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    page.locator(f'[data-open="{order["id"]}"]').click()
    page.get_by_label("Repair status").select_option(label="Repairing")
    page.get_by_text("Repairing", exact=True).first.wait_for()
    assert page.locator(".history-item").count() == 2
    assert page.locator(".history-item").last.get_by_text("Repairing", exact=True).is_visible()
    page.get_by_role("button", name="Dashboard").click()
    assert page.get_by_text("Active orders", exact=True).is_visible()
