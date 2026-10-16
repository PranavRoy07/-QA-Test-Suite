"""SauceDemo doesn't expose a free-text search box; its equivalent
'filter real data' surface is the product sort dropdown (name A-Z/Z-A,
price low-high/high-low). These tests cover that control, which is the
roadmap's 'search and filter' item for this target app. See docs/TEST_PLAN.md
for the explicit scope note.
"""
import pytest
from playwright.sync_api import Page
from pages.inventory_page import InventoryPage


@pytest.mark.regression
def test_sort_name_a_to_z(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    inventory.sort_by("az")
    names = inventory.item_names()
    assert names == sorted(names)


@pytest.mark.regression
def test_sort_name_z_to_a(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    inventory.sort_by("za")
    names = inventory.item_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.regression
def test_sort_price_low_to_high(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    inventory.sort_by("lohi")
    prices = inventory.item_prices()
    assert prices == sorted(prices)


@pytest.mark.regression
def test_sort_price_high_to_low(logged_in_page: Page):
    inventory = InventoryPage(logged_in_page)
    inventory.sort_by("hilo")
    prices = inventory.item_prices()
    assert prices == sorted(prices, reverse=True)
