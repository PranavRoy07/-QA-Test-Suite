"""Shared Playwright fixtures for the UI test suite.

Base URL and headless mode are configurable via environment variables so the
same suite runs locally (headed, for debugging) and in CI (headless).
"""
from __future__ import annotations
import os
import pytest
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

BASE_URL = os.environ.get("BASE_URL", "https://www.saucedemo.com")
HEADLESS = os.environ.get("HEADLESS", "true").lower() != "false"

STANDARD_USER = "standard_user"
LOCKED_OUT_USER = "locked_out_user"
PROBLEM_USER = "problem_user"
ERROR_USER = "error_user"
VALID_PASSWORD = "secret_sauce"


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance) -> Browser:
    browser = playwright_instance.chromium.launch(headless=HEADLESS)
    yield browser
    browser.close()


@pytest.fixture()
def context(browser: Browser) -> BrowserContext:
    context = browser.new_context(base_url=BASE_URL, viewport={"width": 1280, "height": 800})
    yield context
    context.close()


@pytest.fixture()
def page(context: BrowserContext) -> Page:
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture()
def logged_in_page(page: Page) -> Page:
    """A page already authenticated as the standard (bug-free) user,
    landed on the inventory listing, with the product grid actually
    rendered (not just the URL changed) before handing off to the test."""
    page.goto("/")
    page.locator("#user-name").fill(STANDARD_USER)
    page.locator("#password").fill(VALID_PASSWORD)
    page.locator("#login-button").click()
    page.wait_for_url("**/inventory.html")
    page.locator(".inventory_item").first.wait_for(state="visible")
    return page
