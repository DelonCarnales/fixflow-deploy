import re
from playwright.sync_api import sync_playwright

checks = []
errors = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 1000})
    page.on("pageerror", lambda error: errors.append(str(error)))

    def collect_console_error(message):
        if message.type != "error":
            return
        url = message.location.get("url", "")
        # The unknown-order lookup intentionally returns HTTP 404. The UI handles it.
        if url.endswith("/public/orders/FF-9999") and "404" in message.text:
            return
        errors.append(f"{message.text} at {message.location}")

    page.on("console", collect_console_error)
    page.goto("http://127.0.0.1:8000", wait_until="networkidle")

    page.get_by_role("heading", name="Good afternoon").wait_for()
    assert page.get_by_text("Active orders", exact=True).is_visible()
    assert page.get_by_text("Waiting for parts", exact=True).first.is_visible()
    assert page.get_by_text("Ready for pickup", exact=True).first.is_visible()
    assert page.get_by_text("Completed", exact=True).first.is_visible()
    assert page.get_by_text("Live backend", exact=True).is_visible()
    assert page.get_by_text("FF-1001", exact=True).first.is_visible()
    checks.append("dashboard loads from the API with all summary cards")

    page.get_by_role("button", name=re.compile("Repair orders")).click()
    page.get_by_role("textbox", name="Search repair orders").fill("MacBook")
    assert page.get_by_text("FF-1002", exact=True).is_visible()
    assert page.get_by_text("FF-1001", exact=True).count() == 0
    checks.append("order search filters the table")

    page.get_by_role("textbox", name="Search repair orders").fill("")
    page.get_by_label("Filter by status").select_option(label="Ready for pickup")
    assert page.get_by_text("FF-1003", exact=True).is_visible()
    assert page.get_by_text("FF-1002", exact=True).count() == 0
    checks.append("status filter works")

    page.get_by_role("button", name=re.compile("New repair order")).click()
    dialog = page.get_by_role("dialog", name="New repair order")
    dialog.get_by_role("button", name="Create order").click()
    assert "Customer name is required." in page.get_by_role("alert").inner_text()
    assert "Device model is required." in page.get_by_role("alert").inner_text()
    checks.append("required fields show validation")

    dialog.locator('input[name="customerName"]').fill("Test Customer")
    dialog.locator('input[name="phone"]').fill("+7 777 111 22 33")
    dialog.locator('input[name="deviceModel"]').fill("Test Notebook")
    dialog.locator('textarea[name="problem"]').fill("Does not turn on")
    dialog.locator('input[name="estimatedCost"]').fill("10000")
    dialog.get_by_role("button", name="Create order").click()
    page.get_by_role("heading", name="Test Notebook").wait_for()
    assert page.get_by_text(re.compile("FF-1006")).is_visible()
    checks.append("valid order can be created")

    page.get_by_role("button", name="Edit order details").click()
    cancel_dialog = page.get_by_role("dialog", name="Edit repair order")
    cancel_dialog.locator('input[name="customerName"]').fill("Canceled Change")
    cancel_dialog.get_by_role("button", name="Cancel").click()
    assert page.get_by_text("Test Customer", exact=True).is_visible()
    checks.append("canceling an edit does not save changes")

    page.get_by_role("button", name="Edit order details").click()
    edit_dialog = page.get_by_role("dialog", name="Edit repair order")
    edit_dialog.locator('input[name="customerName"]').fill("Updated Test Customer")
    edit_dialog.locator('input[name="deviceModel"]').fill("Updated Notebook")
    edit_dialog.get_by_role("button", name="Save changes").click()
    page.get_by_role("heading", name="Updated Notebook").wait_for()
    assert page.get_by_text("Updated Test Customer", exact=True).is_visible()
    checks.append("editing order saves changed values")

    # Refresh the page to make sure the changes were saved by the backend.
    page.reload(wait_until="networkidle")
    page.get_by_role("heading", name="Good afternoon").wait_for()
    page.get_by_role("button", name=re.compile("Repair orders")).click()
    page.get_by_role("textbox", name="Search repair orders").fill("Updated Notebook")
    assert page.get_by_text("FF-1006", exact=True).is_visible()
    page.get_by_role("button", name=re.compile("FF-1006")).click()
    page.get_by_role("heading", name="Updated Notebook").wait_for()
    assert page.get_by_text("Updated Test Customer", exact=True).is_visible()
    checks.append("edited order stays saved after a browser refresh")

    page.get_by_label("Repair status").select_option(label="Repairing")
    page.locator(".history-item strong").filter(has_text="Repairing").last.wait_for()
    assert page.locator(".detail-heading .status").inner_text() == "Repairing"
    checks.append("status change updates current status and history")

    page.get_by_role("button", name=re.compile("Spare parts")).click()
    page.get_by_role("button", name=re.compile("Add part")).click()
    part_dialog = page.get_by_role("dialog", name="Add spare part")
    part_dialog.locator('input[name="name"]').fill("HDMI cable")
    part_dialog.locator('input[name="stock"]').fill("3")
    part_dialog.locator('input[name="unitPrice"]').fill("1200")
    part_dialog.get_by_role("button", name="Add part").click()
    page.get_by_text("HDMI cable", exact=True).wait_for()
    checks.append("new spare part can be added")

    row = page.locator("tr").filter(has_text="Laptop fan").first
    row.get_by_role("button", name="Edit").click()
    part_edit = page.get_by_role("dialog", name="Edit spare part")
    part_edit.locator('input[name="name"]').fill("Fan for laptops")
    part_edit.get_by_role("button", name="Save part").click()
    page.get_by_text("Fan for laptops", exact=True).wait_for()
    assert page.get_by_text("PT-01", exact=True).is_visible()
    checks.append("spare part can be renamed without changing its ID")

    page.get_by_role("button", name=re.compile("Customer lookup")).click()
    page.locator("#lookup-number").fill("FF-1003")
    page.get_by_role("button", name="Check status").click()
    ready_message = page.get_by_text("Your device is ready. Please contact the shop to arrange pickup.")
    ready_message.wait_for(state="visible")
    assert ready_message.is_visible()
    page.locator("#lookup-number").fill("FF-9999")
    page.get_by_role("button", name="Check status").click()
    page.get_by_role("alert").wait_for(state="visible")
    assert page.get_by_role("alert").is_visible()
    checks.append("customer lookup handles known and unknown order numbers")

    page.set_viewport_size({"width": 390, "height": 844})
    assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth")
    checks.append("mobile viewport has no page-level horizontal overflow")
    page.close()

    # A backend outage should show a readable message instead of breaking the page.
    error_page = browser.new_page(viewport={"width": 1280, "height": 900})
    error_page.route("http://127.0.0.1:8000/orders**", lambda route: route.abort())
    error_page.route("http://127.0.0.1:8000/parts**", lambda route: route.abort())
    error_page.goto("http://127.0.0.1:8000", wait_until="networkidle")
    error_page.get_by_text(re.compile("Could not connect to the backend")).wait_for(state="visible")
    checks.append("backend connection failure shows a readable message")
    error_page.close()
    browser.close()

if errors:
    raise AssertionError("Browser console errors: " + "; ".join(errors))

for check in checks:
    print("PASS:", check)
print(f"TOTAL: {len(checks)} browser checks passed")
