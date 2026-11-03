from e2e.helpers import create_order, unique_name


def test_search_filters_by_order_customer_and_device(page, base_url):
    customer = unique_name("SearchCustomer")
    order = create_order(page, customer=customer, model=unique_name("SearchDevice"))
    page.goto(base_url, wait_until="networkidle")
    page.get_by_role("button", name="Repair orders").click()
    search = page.get_by_role("textbox", name="Search repair orders")
    search.fill(order["id"])
    assert page.get_by_text(order["id"], exact=True).is_visible()
    search.fill(customer)
    assert page.get_by_text(order["id"], exact=True).is_visible()
    search.fill(order["deviceModel"])
    assert page.get_by_text(order["id"], exact=True).is_visible()
    search.fill("no-such-order-e2e")
    assert page.get_by_text("No repair orders found", exact=False).is_visible()
