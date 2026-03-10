import pytest                                       # pytest is the testing framework — needed for @pytest.mark.parametrize and pytest.param
from pages.login_page import LoginPage             # import the LoginPage class which handles all interactions with the login screen
from pages.inventory_page import InventoryPage     # import the InventoryPage class which handles all interactions with the products page


def test_login_success(driver):
    # test that a valid user can log in and land on the inventory page
    login = LoginPage(driver)                      # create a LoginPage object — passes the browser driver so the page can control it
    login.open()                                   # navigate the browser to the login URL
    login.login("standard_user", "secret_sauce")   # type credentials and click Login

    inventory = InventoryPage(driver)              # create an InventoryPage object to interact with the page we should now be on
    assert inventory.is_loaded()                   # assert that the browser is now on the inventory page URL
    assert inventory.get_title() == "Products"     # assert that the page heading text is exactly "Products"


def test_invalid_login(driver):
    # test that logging in with wrong credentials shows an error message
    login = LoginPage(driver)
    login.open()
    login.login("invalid_user", "invalid_password")  # attempt login with credentials that do not exist

    # assert that the error banner contains the expected message
    # using 'in' instead of == because the full message is long — we only check the key phrase
    assert "Username and password do not match" in login.get_error_message()


def test_inventory_has_six_items(driver):
    # test that the inventory page shows exactly 6 products after a successful login
    login = LoginPage(driver)
    login.open()
    login.login("standard_user", "secret_sauce")

    inventory = InventoryPage(driver)
    assert inventory.get_item_count() == 6         # SauceDemo always has exactly 6 products on the inventory page


@pytest.mark.parametrize("username, password, expected_url, expected_error", [
    # each pytest.param is one test case — id= sets the readable name shown in the test output
    pytest.param("standard_user",   "secret_sauce",   "inventory", None,                                    id="valid_user"),
    # valid credentials → should redirect to inventory, no error expected (None)

    pytest.param("locked_out_user", "secret_sauce",   None,        "Sorry, this user has been locked out.", id="locked_user"),
    # SauceDemo has a built-in locked account — should show a specific lock-out error

    pytest.param("standard_user",   "wrong_password", None,        "Username and password do not match",    id="wrong_password"),
    # correct username but wrong password → should show a mismatch error

    pytest.param("wrong_user",      "wrong_password", None,        "Username and password do not match",    id="wrong_user"),
    # both username and password are wrong → same mismatch error

    pytest.param("",                "",               None,        "Username is required",                  id="empty_credentials"),
    # both fields empty → should show "Username is required" (checked first)

    pytest.param("standard_user",   "",               None,        "Password is required",                  id="missing_password"),
    # username filled but password empty → should show "Password is required"
])
def test_login_scenarios(driver, username, password, expected_url, expected_error):
    # this single test function runs 6 times — once for each pytest.param row above
    login = LoginPage(driver)
    login.open()                                   # navigate to the login page for each scenario
    login.login(username, password)                # attempt login with the current row's credentials

    if expected_url:
        # if expected_url is not None, login should have succeeded — check the browser redirected correctly
        assert expected_url in driver.current_url
    else:
        # if expected_url is None, login should have failed — check the correct error message is displayed
        assert expected_error in login.get_error_message()
