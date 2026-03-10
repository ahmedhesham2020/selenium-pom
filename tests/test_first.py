from selenium.webdriver.common.by import By                        # By provides the strategy constants used to locate elements (ID, CSS, etc.)
from selenium.webdriver.support.ui import WebDriverWait            # WebDriverWait pauses execution until a condition is met or a timeout expires
from selenium.webdriver.support import expected_conditions as EC   # EC is a collection of ready-made wait conditions

URL = "https://www.saucedemo.com"                  # base URL of the SauceDemo website — stored as a constant so every test uses the same value


def test_saucedemo_title(driver):
    # test that the browser tab title contains "Swag Labs" when the login page loads
    driver.get(URL)                                # navigate the browser to the SauceDemo homepage
    assert "Swag Labs" in driver.title             # driver.title returns the current page's <title> tag text


def test_saucedemo_login_visible(driver):
    # test that navigating to the URL lands on the correct page (URL check only)
    driver.get(URL)
    # assert the current URL exactly matches the expected address (with trailing slash)
    assert driver.current_url == "https://www.saucedemo.com/"


def test_login_with_valid_user(driver):
    # test that submitting valid credentials redirects to the inventory page
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")   # find the username field by its id and type into it
    driver.find_element(By.ID, "password").send_keys("secret_sauce")     # find the password field by its id and type into it
    driver.find_element(By.ID, "login-button").click()                    # find the Login button by its id and click it

    wait = WebDriverWait(driver, 10)               # create a wait object with a 10-second timeout
    wait.until(EC.url_contains("inventory"))       # pause until the URL contains "inventory" — confirms the redirect happened

    assert driver.current_url == "https://www.saucedemo.com/inventory.html"  # verify the final URL is exactly the inventory page


def test_login_with_wrong_password(driver):
    # test that submitting a wrong password shows an error message
    driver.get(URL)
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")   # intentionally wrong password
    driver.find_element(By.ID, "login-button").click()

    wait = WebDriverWait(driver, 10)
    # wait until the error element is visible — CSS selector targets any element with data-test="error"
    error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))

    assert "Username and password do not match" in error.text             # verify the error text contains the expected phrase


def test_login_success(driver):
    # same as test_login_with_valid_user but uses explicit waits for every interaction
    # explicit waits are more reliable than direct find_element because they retry until the element is ready
    driver.get(URL)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")  # wait until field is clickable, then type
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys("secret_sauce")    # wait until field is clickable, then type
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()                  # wait until button is clickable, then click

    wait.until(EC.url_contains("inventory"))       # wait for the redirect to complete
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"


def test_login_error_message(driver):
    # test that an error message appears when wrong credentials are submitted, using explicit waits throughout
    driver.get(URL)
    wait = WebDriverWait(driver, 10)

    wait.until(EC.element_to_be_clickable((By.ID, "user-name"))).send_keys("standard_user")
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys("wrong_password")  # wrong password to trigger the error
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    # wait until the error banner is visible, then capture it as an element
    error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    assert "Username and password do not match" in error.text             # verify the error text matches the expected phrase
