import os
from pathlib import Path

import pytest

BASE_URL = os.getenv("E2E_BASE_URL", "http://localhost:8000").rstrip("/")
ARTIFACTS = Path("test-results")


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def page(browser, request):
    ARTIFACTS.mkdir(exist_ok=True)
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page = context.new_page()
    errors = []

    def on_page_error(error):
        errors.append(str(error))

    def on_console(message):
        if message.type == "error":
            # The customer lookup intentionally handles unknown-order HTTP 404s.
            url = message.location.get("url", "")
            if url.endswith("/public/orders/FF-9999") and "404" in message.text:
                return
            errors.append(f"{message.text} ({url})")

    page.on("pageerror", on_page_error)
    page.on("console", on_console)
    request.node._browser_page = page
    request.node._browser_context = context
    request.node._browser_errors = errors
    yield page
    context.close()


def pytest_runtest_makereport(item, call):
    if call.when != "call" or call.excinfo is None:
        return
    page = getattr(item, "_browser_page", None)
    context = getattr(item, "_browser_context", None)
    if page is not None:
        page.screenshot(path=str(ARTIFACTS / f"{item.name}.png"), full_page=True)
    if context is not None:
        context.tracing.stop(path=str(ARTIFACTS / f"{item.name}.zip"))


@pytest.fixture(autouse=True)
def fail_on_unexpected_browser_errors(request):
    yield
    errors = getattr(request.node, "_browser_errors", [])
    if errors:
        pytest.fail("Unexpected browser errors:\n" + "\n".join(errors))
