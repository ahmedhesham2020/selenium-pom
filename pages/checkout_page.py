from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CheckoutPage:
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT  = (By.ID, "last-name")
    ZIP_CODE_INPUT   = (By.ID, "postal-code")
    CONTINUE_BUTTON  = (By.ID, "continue")
    FINISH_BUTTON    = (By.ID, "finish")
    COMPLETE_HEADER  = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 10)

    def _react_input(self, element, value):
        """Set value on a React controlled input and trigger its onChange."""
        self.driver.execute_script("""
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        """, element, value)

    def fill_info(self, first_name, last_name, zip_code):
        fn = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_INPUT))
        ln = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_INPUT))
        pc = self.wait.until(EC.element_to_be_clickable(self.ZIP_CODE_INPUT))
        self._react_input(fn, first_name)
        self._react_input(ln, last_name)
        self._react_input(pc, zip_code)

    def click_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def click_finish(self):
        self.wait.until(EC.url_contains("step-two"))
        btn = self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))
        self.driver.execute_script("arguments[0].click();", btn)

    def get_complete_header(self):
        return self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER)).text
