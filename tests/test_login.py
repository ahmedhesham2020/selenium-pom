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
