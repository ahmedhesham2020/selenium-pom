from selenium.webdriver.common.by import By                        # By provides the strategy constants used to locate elements
from selenium.webdriver.support.ui import WebDriverWait            # WebDriverWait pauses execution until a condition is met or a timeout expires
from selenium.webdriver.support import expected_conditions as EC   # EC is a collection of ready-made wait conditions


class CartPage:
    # ── URL ────────────────────────────────────────────────────────────────────
    URL = "https://www.saucedemo.com/cart.html"    # the full address of the cart page

    # ── Locators ───────────────────────────────────────────────────────────────
    CART_ITEM      = (By.CLASS_NAME, "cart_item")                       # each item row inside the cart
    CHECKOUT_BUTTON = (By.ID, "checkout")                               # the Checkout button that starts the checkout flow
    REMOVE_BUTTON  = (By.CSS_SELECTOR, ".cart_item .btn_secondary")     # the Remove button inside each cart item row

    # ── Constructor ────────────────────────────────────────────────────────────
    def __init__(self, driver):
        self.driver = driver                       # store the WebDriver instance so all methods can control the browser
        self.wait   = WebDriverWait(driver, 10)    # create a wait object with a 10-second timeout

    # ── Actions ────────────────────────────────────────────────────────────────
    def open(self):
        self.driver.get(self.URL)                  # navigate directly to the cart page by URL

    def get_item_count(self):
        self.wait.until(EC.url_contains("cart"))   # wait until the browser is on the cart page before looking for items

        # find_elements (plural) returns a list of ALL elements matching the locator
        # the * unpacks the tuple (By.CLASS_NAME, "cart_item") into two separate arguments
        # if no items exist it returns an empty list — no exception is raised
        items = self.driver.find_elements(*self.CART_ITEM)
        return len(items)                          # count how many cart item rows are on the page

    def click_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))  # wait until the Checkout button is clickable
        self.driver.execute_script("arguments[0].click();", btn)                  # JS click to avoid macOS silent click failure
