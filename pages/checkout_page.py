from selenium.webdriver.common.by import By                        # By provides the strategy constants used to locate elements
from selenium.webdriver.support.ui import WebDriverWait            # WebDriverWait pauses execution until a condition is met or a timeout expires
from selenium.webdriver.support import expected_conditions as EC   # EC is a collection of ready-made wait conditions


class CheckoutPage:
    # ── Locators ───────────────────────────────────────────────────────────────
    # The checkout flow spans two pages (step-one and step-two) but we use one class
    # because they are part of the same user journey.
    FIRST_NAME_INPUT = (By.ID, "first-name")       # first name text field on checkout step one
    LAST_NAME_INPUT  = (By.ID, "last-name")        # last name text field on checkout step one
    ZIP_CODE_INPUT   = (By.ID, "postal-code")      # zip/postal code text field on checkout step one
    CONTINUE_BUTTON  = (By.ID, "continue")         # Continue button that moves from step one to step two
    FINISH_BUTTON    = (By.ID, "finish")           # Finish button on step two that completes the order
    COMPLETE_HEADER  = (By.CLASS_NAME, "complete-header")  # the "Thank you for your order!" text shown after a successful order

    # ── Constructor ────────────────────────────────────────────────────────────
    def __init__(self, driver):
        self.driver = driver                       # store the WebDriver instance so all methods can control the browser
        self.wait   = WebDriverWait(driver, 10)    # create a wait object with a 10-second timeout

    # ── Private Helpers ────────────────────────────────────────────────────────
    def _react_input(self, element, value):
        # SauceDemo checkout uses React controlled inputs.
        # React manages input values through its own internal state, not the raw DOM.
        # send_keys() types into the DOM but does NOT trigger React's onChange event,
        # so React's state stays empty and form validation fails (see faced_issues.txt Issue 8).
        #
        # This JavaScript approach works in two steps:
        #   1. Use the browser's native setter to change the DOM value, bypassing React's override
        #   2. Fire a native 'input' event that React listens to, forcing it to update its state
        self.driver.execute_script("""
            var nativeInputValueSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value').set;
            nativeInputValueSetter.call(arguments[0], arguments[1]);
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
        """, element, value)
        # arguments[0] = the input element, arguments[1] = the value to set
        # bubbles: true means the event travels up the DOM tree so React's listener catches it

    # ── Actions ────────────────────────────────────────────────────────────────
    def fill_info(self, first_name, last_name, zip_code):
        # wait until each field is clickable (meaning the page is loaded and the field is ready)
        fn = self.wait.until(EC.element_to_be_clickable(self.FIRST_NAME_INPUT))  # first name field element
        ln = self.wait.until(EC.element_to_be_clickable(self.LAST_NAME_INPUT))   # last name field element
        pc = self.wait.until(EC.element_to_be_clickable(self.ZIP_CODE_INPUT))    # zip code field element

        # fill each field using the React-safe helper instead of send_keys
        self._react_input(fn, first_name)
        self._react_input(ln, last_name)
        self._react_input(pc, zip_code)

    def click_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))  # wait until Continue is clickable
        self.driver.execute_script("arguments[0].click();", btn)                  # JS click to avoid macOS silent click failure

    def click_finish(self):
        # JS click fires and returns immediately — the browser still needs time to navigate
        # from step-one to step-two. If we search for FINISH_BUTTON right away it won't exist yet.
        # Waiting for the URL to contain "step-two" guarantees the new page is loaded before we proceed.
        self.wait.until(EC.url_contains("step-two"))

        btn = self.wait.until(EC.element_to_be_clickable(self.FINISH_BUTTON))    # now it's safe to look for the Finish button
        self.driver.execute_script("arguments[0].click();", btn)                  # JS click to avoid macOS silent click failure

    def get_complete_header(self):
        # wait until the confirmation header is visible on the order-complete page, then return its text
        return self.wait.until(EC.visibility_of_element_located(self.COMPLETE_HEADER)).text
