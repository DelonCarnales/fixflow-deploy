from e2e.helpers import create_order, unique_name


def test_edit_order_keeps_id_and_does_not_add_history_for_text_edits(page, base_url):
    order = create_order(page)
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    page.locator(f'[data-open="{order["id"]}"]').click()
    page.get_by_role("button", name="Edit order details").click()
    dialog = page.get_by_role("dialog", name="Edit repair order")
    assert dialog.locator('input[name="customerName"]').input_value() == order["customerName"]
    history_count = page.locator(".history-item").count()
    changed = unique_name("EditedDevice")
    dialog.locator('input[name="deviceModel"]').fill(changed)
    dialog.get_by_role("button", name="Save changes").click()
    page.get_by_role("heading", name=changed).wait_for()
    assert page.get_by_text(order["id"], exact=False).count() >= 1
    assert page.locator(".history-item").count() == history_count
    page.get_by_role("button", name="Edit order details").click()
    dialog = page.get_by_role("dialog", name="Edit repair order")
    dialog.locator('input[name="customerName"]').fill("Discarded Name")
    dialog.get_by_role("button", name="Cancel").click()
    assert page.get_by_text(order["customerName"], exact=True).is_visible()
    page.get_by_role("button", name="Edit order details").click()
    dialog = page.get_by_role("dialog", name="Edit repair order")
    dialog.locator('input[name="customerName"]').fill("Closed Dialog Name")
    dialog.get_by_role("button", name="Close form").click()
    assert page.get_by_text(order["customerName"], exact=True).is_visible()
