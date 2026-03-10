from selenium.webdriver.common.by import By                        # By provides the strategy constants used to locate elements (ID, CSS, XPATH, etc.)
from selenium.webdriver.support.ui import WebDriverWait            # WebDriverWait pauses execution until a condition is met or a timeout expires
from selenium.webdriver.support import expected_conditions as EC   # EC is a collection of ready-made conditions (element visible, clickable, URL contains, etc.)


class LoginPage:
    # ── URL ────────────────────────────────────────────────────────────────────
    URL = "https://www.saucedemo.com/"             # the full address of the login page — stored as a class variable so every method can use it

    # ── Locators ───────────────────────────────────────────────────────────────
    # Each locator is a tuple of (strategy, value). Storing them here means if
    # the HTML ever changes we only update one line, not every method that uses it.
    USERNAME_INPUT = (By.ID, "user-name")          # the username text field — located by its HTML id attribute
    PASSWORD_INPUT = (By.ID, "password")           # the password text field — located by its HTML id attribute
    LOGIN_BUTTON   = (By.ID, "login-button")       # the Login button — located by its HTML id attribute
    ERROR_MESSAGE  = (By.CSS_SELECTOR, "[data-test='error']")  # the red error banner — CSS selector targets any element whose data-test attribute equals 'error'

    # ── Constructor ────────────────────────────────────────────────────────────
    def __init__(self, driver):
        self.driver = driver                       # store the WebDriver instance so all methods in this class can control the browser
        self.wait   = WebDriverWait(driver, 10)    # create a wait object with a 10-second timeout — reused by every method instead of creating a new one each time

    # ── Actions ────────────────────────────────────────────────────────────────
    def open(self):
        self.driver.get(self.URL)                  # navigate the browser to the login page URL

    def enter_username(self, username):
        # wait until the username field is visible, then type the given value into it
        self.wait.until(EC.visibility_of_element_located(self.USERNAME_INPUT)).send_keys(username)

    def enter_password(self, password):
        # wait until the password field is visible, then type the given value into it
        self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT)).send_keys(password)

    def click_login(self):
        # wait until the Login button can be clicked, then click it
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()

    def get_error_message(self):
        # wait until the red error banner is visible, then return its text content
        return self.wait.until(EC.visibility_of_element_located(self.ERROR_MESSAGE)).text

    def login(self, username, password):
        self.enter_username(username)              # type the username into the field
        self.enter_password(password)              # type the password into the field
        self.click_login()                         # click the Login button

        # wait until one of two things happens:
        #   1. the URL contains "inventory" — login succeeded and we were redirected
        #   2. the error element appears in the DOM — login failed and an error is shown
        # using a lambda (anonymous function) because this condition is not in the EC library
        self.wait.until(lambda d: "inventory" in d.current_url or
                        len(d.find_elements(*self.ERROR_MESSAGE)) > 0)
