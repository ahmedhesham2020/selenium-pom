import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


def test_login_success(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.is_loaded()
    assert inventory.get_title() == "Products"


def test_invalid_login(driver):
    login = LoginPage(driver)
    login.open()
    login.login("invalid_user", "invalid_password")
    assert "Username and password do not match" in login.get_error_message()


def test_inventory_has_six_items(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.get_item_count() == 6


@pytest.mark.parametrize("username, password, expected_url, expected_error", [
    pytest.param("standard_user",  "secret_sauce",   "inventory", None,                                         id="valid_user"),
    pytest.param("locked_out_user","secret_sauce",   None,        "Sorry, this user has been locked out.",      id="locked_user"),
    pytest.param("standard_user",  "wrong_password", None,        "Username and password do not match",         id="wrong_password"),
    pytest.param("wrong_user",     "wrong_password", None,        "Username and password do not match",         id="wrong_user"),
    pytest.param("",               "",               None,        "Username is required",                       id="empty_credentials"),
    pytest.param("standard_user",  "",               None,        "Password is required",                       id="missing_password"),
])
def test_login_scenarios(driver, username, password, expected_url, expected_error):
    login = LoginPage(driver)
    login.open()
    login.login(username, password)

    if expected_url:
        assert expected_url in driver.current_url
    else:
        assert expected_error in login.get_error_message()
