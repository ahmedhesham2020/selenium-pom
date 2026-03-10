from selenium.webdriver.common.by import By                        # By provides the strategy constants used to locate elements
from selenium.webdriver.support.ui import WebDriverWait            # WebDriverWait pauses execution until a condition is met or a timeout expires
from selenium.webdriver.support import expected_conditions as EC   # EC is a collection of ready-made wait conditions


class InventoryPage:
    # ── URL ────────────────────────────────────────────────────────────────────
    URL = "https://www.saucedemo.com/inventory.html"  # the full address of the products page after login

    # ── Locators ───────────────────────────────────────────────────────────────
    TITLE          = (By.CLASS_NAME, "title")              # the "Products" heading at the top of the page
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")     # each product card — there are 6 on the page
    CART_BADGE     = (By.CLASS_NAME, "shopping_cart_badge")# the red number bubble on the cart icon showing how many items are in the cart
    CART_LINK      = (By.CLASS_NAME, "shopping_cart_link") # the cart icon in the top-right corner — clicking it goes to the cart page

    # ── Constructor ────────────────────────────────────────────────────────────
    def __init__(self, driver):
        self.driver = driver                       # store the WebDriver instance so all methods can control the browser
        self.wait   = WebDriverWait(driver, 10)    # create a wait object with a 10-second timeout

    # ── Actions ────────────────────────────────────────────────────────────────
    def is_loaded(self):
        self.wait.until(EC.url_contains("inventory"))      # wait until the browser URL contains "inventory" — confirms the page loaded after login
        return self.driver.current_url == self.URL         # return True if the current URL exactly matches the inventory page URL

    def get_title(self):
        # wait until the "Products" heading is visible on screen, then return its text
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def get_item_count(self):
        # wait until at least one product card is present in the DOM, then count how many there are
        items = self.wait.until(EC.presence_of_all_elements_located(self.INVENTORY_ITEM))
        return len(items)                          # len() counts the number of elements in the list — should be 6 on SauceDemo

    def add_first_item_to_cart(self):
        # CSS selector: find any element whose data-test attribute starts with "add-to-cart"
        # the ^ symbol in CSS means "starts with" — this matches the first Add to Cart button on the page
        add_button = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")

        btn = self.wait.until(EC.element_to_be_clickable(add_button))  # wait until the button is clickable

        # use JavaScript to click instead of .click() because on macOS, native Selenium clicks
        # can be silently ignored by the browser for certain elements (see faced_issues.txt Issue 7)
        self.driver.execute_script("arguments[0].click();", btn)
        # arguments[0] refers to the first argument passed after the JS string — in this case, btn

    def get_cart_badge_count(self):
        # wait until the red cart badge is visible, then convert its text (e.g. "1") to an integer
        return int(self.wait.until(EC.visibility_of_element_located(self.CART_BADGE)).text)

    def go_to_cart(self):
        link = self.wait.until(EC.element_to_be_clickable(self.CART_LINK))  # wait until the cart icon is clickable
        self.driver.execute_script("arguments[0].click();", link)            # JS click to avoid macOS silent click failure
