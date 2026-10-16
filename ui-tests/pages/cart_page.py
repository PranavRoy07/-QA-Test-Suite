from __future__ import annotations
from playwright.sync_api import Page
from pages.base_page import BasePage


class CartPage(BasePage):
    URL = "/cart.html"

    CART_ITEM = ".cart_item"
    ITEM_NAME = ".inventory_item_name"
    REMOVE_BTN = "button", "Remove"
    CHECKOUT_BUTTON = "#checkout"
    CONTINUE_SHOPPING_BUTTON = "#continue-shopping"

    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        return "cart.html" in self.page.url

    def item_count(self) -> int:
        return self.page.locator(self.CART_ITEM).count()

    def item_names(self) -> list[str]:
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def remove_item_by_name(self, item_name: str) -> None:
        row = self.page.locator(self.CART_ITEM).filter(has_text=item_name)
        row.get_by_role("button", name="Remove").click()

    def proceed_to_checkout(self) -> None:
        self.click(self.CHECKOUT_BUTTON)
