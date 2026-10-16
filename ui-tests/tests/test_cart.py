import pytest
from playwright.sync_api import Page
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


@pytest.mark.smoke
def test_add_single_item_updates_cart_badge(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    inventory.add_first_item_to_cart()
    assert inventory.cart_count() == 1


@pytest.mark.regression
def test_add_multiple_items_updates_badge_count(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    names = inventory.item_names()
    for name in names[:3]:
        inventory.add_item_to_cart_by_name(name)
    assert inventory.cart_count() == 3


@pytest.mark.regression
def test_cart_page_lists_added_items(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    target_item = inventory.item_names()[0]
    inventory.add_item_to_cart_by_name(target_item)
    inventory.go_to_cart()

    cart = CartPage(logged_in_page)
    assert cart.is_loaded()
    assert cart.item_count() == 1
    assert target_item in cart.item_names()


@pytest.mark.regression
def test_remove_item_from_cart(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    target_item = inventory.item_names()[0]
    inventory.add_item_to_cart_by_name(target_item)
    inventory.go_to_cart()

    cart = CartPage(logged_in_page)
    assert cart.item_count() == 1
    cart.remove_item_by_name(target_item)
    assert cart.item_count() == 0


@pytest.mark.smoke
def test_empty_cart_shows_no_items(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    inventory.go_to_cart()
    cart = CartPage(logged_in_page)
    assert cart.item_count() == 0
