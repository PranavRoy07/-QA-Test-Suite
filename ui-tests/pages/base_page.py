"""Base Page Object — common Playwright actions shared by every page object.

Keeping this logic in one place means individual page objects stay thin
(locators + intent-revealing methods) instead of re-implementing waits,
clicks, and text getters everywhere.
"""
from __future__ import annotations
from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        locator = self.page.locator(selector)
        locator.click()
        locator.fill(value)

    def text_of(self, selector: str) -> str:
        return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        return self.page.locator(selector).is_visible()

    def wait_for_url_contains(self, fragment: str, timeout: int = 5000) -> None:
        self.page.wait_for_url(f"**/*{fragment}*", timeout=timeout)

    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    def expect_text(self, selector: str, text: str) -> None:
        expect(self.page.locator(selector)).to_contain_text(text)

    def expect_count(self, selector: str, count: int) -> None:
        expect(self.page.locator(selector)).to_have_count(count)
