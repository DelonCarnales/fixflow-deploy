from e2e.helpers import unique_name


def test_add_spare_part_and_stock_badges(page, base_url):
    name = unique_name("NewPart")
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Spare parts").click()
    before = int(page.locator(".card-heading p").inner_text().split()[0])
    page.get_by_role("button", name="Add part").click()
    dialog = page.get_by_role("dialog", name="Add spare part")
    dialog.locator('input[name="name"]').fill(name)
    dialog.locator('input[name="stock"]').fill("2")
    dialog.locator('input[name="unitPrice"]').fill("3900")
    dialog.get_by_role("button", name="Add part").click()
    row = page.get_by_role("row").filter(has_text=name)
    row.wait_for()
    part_id = row.locator("td").nth(1).inner_text()
    assert part_id.startswith("PT-")
    assert row.get_by_text("Low stock", exact=True).is_visible()
    assert row.get_by_text("3,900 ₸", exact=True).is_visible()
    assert page.get_by_text(f"{before + 1} types of parts in stock", exact=True).is_visible()
