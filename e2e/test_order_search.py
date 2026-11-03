from e2e.helpers import create_order, unique_name


def test_search_by_id_customer_device_is_case_insensitive_and_clearable(page, base_url):
    customer = unique_name("SearchCustomer")
    order = create_order(page, customer=customer, model=unique_name("SearchDevice"))
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    search = page.get_by_role("textbox", name="Search repair orders")
    search.fill(order["id"].lower())
    assert page.get_by_text(order["id"], exact=True).is_visible()
    search.fill(customer.lower())
    assert page.get_by_text(order["id"], exact=True).is_visible()
    search.fill(order["deviceModel"].lower())
    assert page.get_by_text(order["id"], exact=True).is_visible()
    total = len(page.request.get(base_url + "/orders").json())
    search.fill("no-such-order-e2e")
    assert page.get_by_text("No repair orders match your search.", exact=True).is_visible()
    assert page.get_by_text(f"Showing 0 of {total} orders", exact=True).is_visible()
    search.fill("")
    assert page.locator("tr.clickable-row").count() == total
    assert page.get_by_text(f"Showing {total} of {total} orders", exact=True).is_visible()
