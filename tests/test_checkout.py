from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


def test_add_item_to_cart(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()
    assert inventory.get_cart_badge_count() == 1


def test_full_checkout_flow(driver):
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()

    cart = CartPage(driver)
    assert cart.get_item_count() == 1

    cart.click_checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_info("Ahmed", "Hesham", "12345")
    checkout.click_continue()
    checkout.click_finish()

    assert checkout.get_complete_header() == "Thank you for your order!"
