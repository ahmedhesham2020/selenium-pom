import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()


def test_add_item_to_cart(driver):
    # login
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    # add first item
    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()

    # verify cart badge shows 1
    assert inventory.get_cart_badge_count() == 1


def test_full_checkout_flow(driver):
    # login
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    # add item and go to cart
    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()

    # verify cart has 1 item
    cart = CartPage(driver)
    assert cart.get_item_count() == 1

    # proceed to checkout
    cart.click_checkout()

    # fill in shipping info
    checkout = CheckoutPage(driver)
    checkout.fill_info("Ahmed", "Hesham", "12345")
    checkout.click_continue()
    checkout.click_finish()

    # verify order complete
    assert checkout.get_complete_header() == "Thank you for your order!"