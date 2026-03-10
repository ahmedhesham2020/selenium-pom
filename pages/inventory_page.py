from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class InventoryPage:

    URL = "https://www.saucedemo.com/inventory.html"

    # --- Locators ---
    TITLE          = (By.CLASS_NAME, "title")
    INVENTORY_ITEM = (By.CLASS_NAME, "inventory_item")
    CART_BADGE     = (By.CLASS_NAME, "shopping_cart_badge")
    CART_LINK      = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    # --- Actions ---
    def is_loaded(self):
        self.wait.until(EC.url_contains("inventory"))
        return self.driver.current_url == self.URL

    def get_title(self):
        return self.wait.until(EC.visibility_of_element_located(self.TITLE)).text

    def get_item_count(self):
        items = self.wait.until(EC.presence_of_all_elements_located(self.INVENTORY_ITEM))
        return len(items)

    def add_first_item_to_cart(self):
        add_button = (By.CSS_SELECTOR, "[data-test^='add-to-cart']")
        btn = self.wait.until(EC.element_to_be_clickable(add_button))
        self.driver.execute_script("arguments[0].click();", btn)

    def get_cart_badge_count(self):
        return int(self.wait.until(EC.visibility_of_element_located(self.CART_BADGE)).text)

    def go_to_cart(self):
        link = self.wait.until(EC.element_to_be_clickable(self.CART_LINK))
        self.driver.execute_script("arguments[0].click();", link)
