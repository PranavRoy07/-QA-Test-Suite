import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from conftest import STANDARD_USER, LOCKED_OUT_USER, VALID_PASSWORD


@pytest.mark.smoke
def test_valid_login_lands_on_inventory(page: Page):
    login_page = LoginPage(page).open()
    login_page.login(STANDARD_USER, VALID_PASSWORD)
    page.wait_for_url("**/inventory.html")
    assert "inventory.html" in page.url


@pytest.mark.negative
def test_invalid_password_shows_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login(STANDARD_USER, "wrong_password")
    assert login_page.has_error()
    assert "do not match" in login_page.error_text().lower()


@pytest.mark.negative
def test_locked_out_user_is_blocked(page: Page):
    login_page = LoginPage(page).open()
    login_page.login(LOCKED_OUT_USER, VALID_PASSWORD)
    assert login_page.has_error()
    assert "locked out" in login_page.error_text().lower()


@pytest.mark.negative
def test_empty_username_shows_required_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login("", VALID_PASSWORD)
    assert login_page.has_error()
    assert "username is required" in login_page.error_text().lower()


@pytest.mark.negative
def test_empty_password_shows_required_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login(STANDARD_USER, "")
    assert login_page.has_error()
    assert "password is required" in login_page.error_text().lower()


@pytest.mark.negative
def test_unknown_username_shows_generic_error(page: Page):
    login_page = LoginPage(page).open()
    login_page.login("not_a_real_user", VALID_PASSWORD)
    assert login_page.has_error()
    assert "do not match" in login_page.error_text().lower()
