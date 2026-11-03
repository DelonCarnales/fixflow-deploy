from e2e.helpers import create_part, unique_name


def test_edit_spare_part_keeps_id_and_cancel_discards(page, base_url):
    part = create_part(page, stock=1)
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Spare parts").click()
    row = page.get_by_role("row").filter(has_text=part["name"])
    row.get_by_role("button", name="Edit").click()
    dialog = page.get_by_role("dialog", name="Edit spare part")
    assert dialog.locator('input[name="name"]').input_value() == part["name"]
    changed = unique_name("EditedPart")
    dialog.locator('input[name="name"]').fill(changed)
    dialog.locator('input[name="stock"]').fill("8")
    dialog.locator('input[name="unitPrice"]').fill("5100")
    dialog.get_by_role("button", name="Save part").click()
    updated = page.get_by_role("row").filter(has_text=changed)
    assert updated.locator("td").nth(1).inner_text() == part["id"]
    assert updated.get_by_text("In stock", exact=True).is_visible()
    updated.get_by_role("button", name="Edit").click()
    dialog = page.get_by_role("dialog", name="Edit spare part")
    dialog.locator('input[name="name"]').fill("Discarded Part")
    dialog.get_by_role("button", name="Cancel").click()
    assert page.get_by_text(changed, exact=True).is_visible()
