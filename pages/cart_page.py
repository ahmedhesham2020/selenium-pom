from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    URL = "https://www.saucedemo.com/cart.html"

    CART_ITEM = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    REMOVE_BUTTON = (By.CSS_SELECTOR, ".cart_item .btn_secondary")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def open(self):
        self.driver.get(self.URL)

    def get_item_count(self):
        self.wait.until(EC.url_contains("cart"))
        items = self.driver.find_elements(*self.CART_ITEM)
        return len(items)

    def click_checkout(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CHECKOUT_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    