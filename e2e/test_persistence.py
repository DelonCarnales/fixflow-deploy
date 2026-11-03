from e2e.helpers import create_order, create_part, unique_name


def test_orders_edits_status_and_parts_survive_reload(page, base_url):
    order = create_order(page)
    part = create_part(page)
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    page.locator(f'[data-open="{order["id"]}"]').click()
    page.get_by_role("button", name="Edit order details").click()
    dialog = page.get_by_role("dialog", name="Edit repair order")
    changed_model = unique_name("PersistedModel")
    dialog.locator('input[name="deviceModel"]').fill(changed_model)
    dialog.get_by_role("button", name="Save changes").click()
    page.get_by_label("Repair status").select_option(label="Repairing")
    page.reload(wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    page.locator(f'[data-open="{order["id"]}"]').click()
    assert page.get_by_role("heading", name=changed_model).is_visible()
    assert page.locator(".history-item").last.get_by_text("Repairing", exact=True).is_visible()
    page.get_by_role("button", name="Spare parts").click()
    assert page.get_by_text(part["name"], exact=True).is_visible()
