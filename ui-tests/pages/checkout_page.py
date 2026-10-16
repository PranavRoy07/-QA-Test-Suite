from __future__ import annotations
from playwright.sync_api import Page
from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    """Customer information form."""

    URL = "/checkout-step-one.html"

    FIRST_NAME_INPUT = "#first-name"
    LAST_NAME_INPUT = "#last-name"
    POSTAL_CODE_INPUT = "#postal-code"
    CONTINUE_BUTTON = "#continue"
    ERROR_MESSAGE = "[data-test='error']"

    def fill_info(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill(self.FIRST_NAME_INPUT, first_name)
        self.fill(self.LAST_NAME_INPUT, last_name)
        self.fill(self.POSTAL_CODE_INPUT, postal_code)

    def continue_to_overview(self) -> None:
        self.click(self.CONTINUE_BUTTON)

    def error_text(self) -> str:
        return self.text_of(self.ERROR_MESSAGE)

    def has_error(self) -> bool:
        return self.is_visible(self.ERROR_MESSAGE)


class CheckoutStepTwoPage(BasePage):
    """Order overview / summary."""

    URL = "/checkout-step-two.html"

    ITEM_TOTAL = ".summary_subtotal_label"
    TAX = ".summary_tax_label"
    TOTAL = ".summary_total_label"
    FINISH_BUTTON = "#finish"

    def finish(self) -> None:
        self.click(self.FINISH_BUTTON)

    def total_text(self) -> str:
        return self.text_of(self.TOTAL)


class CheckoutCompletePage(BasePage):
    """Order confirmation."""

    URL = "/checkout-complete.html"

    COMPLETE_HEADER = ".complete-header"

    def is_order_complete(self) -> bool:
        return self.is_visible(self.COMPLETE_HEADER) and "Thank you" in self.text_of(self.COMPLETE_HEADER)
