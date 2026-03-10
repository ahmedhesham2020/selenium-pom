from pages.login_page import LoginPage             # LoginPage handles all interactions with the login screen
from pages.inventory_page import InventoryPage     # InventoryPage handles all interactions with the products listing page
from pages.cart_page import CartPage               # CartPage handles all interactions with the shopping cart page
from pages.checkout_page import CheckoutPage       # CheckoutPage handles all interactions with the checkout flow (step one and step two)


def test_add_item_to_cart(driver):
    # test that clicking Add to Cart increases the cart badge count to 1
    login = LoginPage(driver)
    login.open()                                   # navigate to the login page
    login.login("standard_user", "secret_sauce")   # log in with valid credentials

    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()             # click the Add to Cart button for the first product

    # assert the red badge on the cart icon now shows "1"
    assert inventory.get_cart_badge_count() == 1


def test_full_checkout_flow(driver):
    # end-to-end test: login → add item → go to cart → checkout → confirm order complete
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")   # log in with valid credentials

    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()             # add one product to the cart
    inventory.go_to_cart()                         # click the cart icon to navigate to the cart page

    cart = CartPage(driver)
    assert cart.get_item_count() == 1              # verify exactly one item is in the cart before proceeding

    cart.click_checkout()                          # click the Checkout button to start the checkout flow

    checkout = CheckoutPage(driver)
    checkout.fill_info("Ahmed", "Hesham", "12345") # fill in the shipping information form (first name, last name, zip code)
    checkout.click_continue()                      # click Continue to move from step one to step two
    checkout.click_finish()                        # click Finish to submit the order

    # assert the confirmation header on the order-complete page shows the expected message
    assert checkout.get_complete_header() == "Thank you for your order!"
