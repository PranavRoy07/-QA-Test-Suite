from __future__ import annotations
from playwright.sync_api import Page
from pages.base_page import BasePage


class InventoryPage(BasePage):
    URL = "/inventory.html"

    INVENTORY_ITEM = ".inventory_item"
    ITEM_NAME = ".inventory_item_name"
    ITEM_PRICE = ".inventory_item_price"
    SORT_DROPDOWN = "[data-test='product-sort-container']"
    CART_BADGE = ".shopping_cart_badge"
    CART_LINK = ".shopping_cart_link"
    ADD_TO_CART_BTN_TEMPLATE = "button[data-test='add-to-cart-{slug}']"

    def __init__(self, page: Page):
        super().__init__(page)

    def is_loaded(self) -> bool:
        return "inventory.html" in self.page.url

    def wait_for_items_loaded(self) -> None:
        """Bulk-query methods like all_inner_texts() don't auto-wait the way
        single-element actions (click, fill) do — they return whatever
        matches at the instant they're called, even an empty list if the
        grid hasn't rendered yet. Call this before any bulk read to avoid
        a flaky empty-list race."""
        self.page.locator(self.INVENTORY_ITEM).first.wait_for(state="visible")

    def item_names(self) -> list[str]:
        self.wait_for_items_loaded()
        return self.page.locator(self.ITEM_NAME).all_inner_texts()

    def item_prices(self) -> list[float]:
        self.wait_for_items_loaded()
        raw = self.page.locator(self.ITEM_PRICE).all_inner_texts()
        return [float(p.replace("$", "")) for p in raw]

    def sort_by(self, option_value: str) -> None:
        # option_value examples: 'az', 'za', 'lohi', 'hilo'
        self.page.locator(self.SORT_DROPDOWN).select_option(option_value)

    def add_first_item_to_cart(self) -> None:
        self.page.locator("button", has_text="Add to cart").first.click()

    def add_item_to_cart_by_name(self, item_name: str) -> None:
        row = self.page.locator(self.INVENTORY_ITEM).filter(has_text=item_name)
        row.get_by_role("button", name="Add to cart").click()

    def cart_count(self) -> int:
        if self.is_visible(self.CART_BADGE):
            return int(self.text_of(self.CART_BADGE))
        return 0

    def go_to_cart(self) -> None:
        self.click(self.CART_LINK)
