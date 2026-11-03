from e2e.helpers import create_part, unique_name


def test_spare_part_form_rejects_empty_and_negative_values(page, base_url):
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Spare parts").click()
    before = page.get_by_role("row").count()
    page.get_by_role("button", name="Add part").click()
    dialog = page.get_by_role("dialog", name="Add spare part")
    dialog.get_by_role("button", name="Add part").click()
    assert "Part name is required." in dialog.get_by_role("alert").inner_text()
    dialog.locator('input[name="name"]').fill(unique_name("Invalid"))
    dialog.locator('input[name="stock"]').fill("-1")
    dialog.locator('input[name="unitPrice"]').fill("-1")
    assert dialog.locator('input[name="stock"]').evaluate("el => !el.checkValidity()")
    assert dialog.locator('input[name="unitPrice"]').evaluate("el => !el.checkValidity()")
    assert page.get_by_role("row").count() == before
