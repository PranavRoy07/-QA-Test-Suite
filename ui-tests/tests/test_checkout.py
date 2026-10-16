import pytest
from playwright.sync_api import Page
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage, CheckoutStepTwoPage, CheckoutCompletePage


def _add_item_and_start_checkout(page: Page) -> None:
    inventory = InventoryPage(page)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()
    CartPage(page).proceed_to_checkout()


@pytest.mark.smoke
def test_full_checkout_happy_path(logged_in_page: Page):
    _add_item_and_start_checkout(logged_in_page)

    step_one = CheckoutStepOnePage(logged_in_page)
    step_one.fill_info("Jane", "Doe", "10001")
    step_one.continue_to_overview()

    step_two = CheckoutStepTwoPage(logged_in_page)
    assert "Total" in step_two.total_text()
    step_two.finish()

    complete = CheckoutCompletePage(logged_in_page)
    assert complete.is_order_complete()


@pytest.mark.regression
def test_checkout_total_includes_tax(logged_in_page: Page):
    _add_item_and_start_checkout(logged_in_page)
    step_one = CheckoutStepOnePage(logged_in_page)
    step_one.fill_info("Jane", "Doe", "10001")
    step_one.continue_to_overview()

    step_two = CheckoutStepTwoPage(logged_in_page)
    subtotal = float(step_two.text_of(step_two.ITEM_TOTAL).split("$")[-1])
    tax = float(step_two.text_of(step_two.TAX).split("$")[-1])
    total = float(step_two.total_text().split("$")[-1])
    assert round(subtotal + tax, 2) == round(total, 2)


@pytest.mark.negative
def test_checkout_requires_first_name(logged_in_page: Page):
    _add_item_and_start_checkout(logged_in_page)
    step_one = CheckoutStepOnePage(logged_in_page)
    step_one.fill_info("", "Doe", "10001")
    step_one.continue_to_overview()
    assert step_one.has_error()
    assert "first name is required" in step_one.error_text().lower()


@pytest.mark.negative
def test_checkout_requires_last_name(logged_in_page: Page):
    _add_item_and_start_checkout(logged_in_page)
    step_one = CheckoutStepOnePage(logged_in_page)
    step_one.fill_info("Jane", "", "10001")
    step_one.continue_to_overview()
    assert step_one.has_error()
    assert "last name is required" in step_one.error_text().lower()


@pytest.mark.negative
def test_checkout_requires_postal_code(logged_in_page: Page):
    _add_item_and_start_checkout(logged_in_page)
    step_one = CheckoutStepOnePage(logged_in_page)
    step_one.fill_info("Jane", "Doe", "")
    step_one.continue_to_overview()
    assert step_one.has_error()
    assert "postal code is required" in step_one.error_text().lower()
