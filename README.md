# Selenium POM — QA Automation Portfolio

![Tests](https://github.com/ahmedhesham2020/selenium-pom/actions/workflows/tests.yml/badge.svg)

End-to-end UI automation framework for [SauceDemo](https://www.saucedemo.com) using Selenium WebDriver and the Page Object Model pattern.

## Skills Demonstrated

| Skill | Where |
|-------|-------|
| Page Object Model (POM) | `pages/` — one class per page |
| Explicit waits (`WebDriverWait` + `EC`) | All page classes |
| Parametrized tests (`pytest.mark.parametrize`) | `test_login.py` → `test_login_scenarios` |
| JavaScript click (macOS/Chrome compatibility) | `inventory_page.py`, `cart_page.py`, `checkout_page.py` |
| React controlled input handling | `checkout_page.py` → `_react_input()` |
| Screenshot on failure | `conftest.py` → `pytest_runtest_makereport` hook |
| Headless CI / visible locally | `conftest.py` → `os.getenv("CI")` |
| Fixture-based driver setup/teardown | `conftest.py` → `driver` fixture |
| Custom markers: smoke + regression | `pytest.ini` + test files |
| GitHub Actions CI/CD | `.github/workflows/tests.yml` |
| HTML test reports | `pytest.ini` → `--html=report.html` |

## Project Structure

```
selenium-pom/
├── conftest.py               # driver fixture, screenshot-on-failure hook
├── pytest.ini                # markers, HTML report, testpaths
├── requirements.txt
├── screenshots/              # auto-populated with PNGs when a test fails
├── pages/
│   ├── login_page.py         # locators + actions for login page
│   ├── inventory_page.py     # locators + actions for inventory page
│   ├── cart_page.py          # locators + actions for cart page
│   └── checkout_page.py      # locators + actions for checkout (step 1 + step 2)
└── tests/
    ├── test_first.py         # basic navigation and title checks
    ├── test_login.py         # login success, invalid login, parametrized scenarios
    └── test_checkout.py      # add to cart, full end-to-end checkout flow
```

## Test Coverage

| File | Tests | What is Covered |
|------|-------|-----------------|
| `test_first.py` | 6 | Page title, URL, login with valid/invalid credentials using raw Selenium |
| `test_login.py` | 9 | Login success, invalid login, item count, 6 parametrized login scenarios |
| `test_checkout.py` | 2 | Add item to cart, full checkout flow end-to-end |
| **Total** | **17** | |

## Parametrized Login Scenarios

| ID | Username | Password | Expected Result |
|----|----------|----------|-----------------|
| `valid_user` | standard_user | secret_sauce | Redirected to inventory |
| `locked_user` | locked_out_user | secret_sauce | "Sorry, this user has been locked out." |
| `wrong_password` | standard_user | wrong_password | "Username and password do not match" |
| `wrong_user` | wrong_user | wrong_password | "Username and password do not match" |
| `empty_credentials` | _(empty)_ | _(empty)_ | "Username is required" |
| `missing_password` | standard_user | _(empty)_ | "Password is required" |

## Screenshot on Failure

When any test fails, a screenshot is automatically saved to `screenshots/<test_name>.png` showing the exact browser state at the moment of failure.

## Running the Tests

```bash
# Install dependencies
pip install -r requirements.txt

# Run full suite
pytest

# Run smoke tests only
pytest -m smoke

# Run regression tests only
pytest -m regression

# Run a specific test file
pytest tests/test_login.py -v
```

## User Flow Covered

```
Login → Add item to cart → Go to cart → Checkout
     → Fill shipping info → Confirm order → Verify completion
```

---

**Author:** Ahmed Hesham — SW Validation Engineer → QA Automation Engineer
**Stack:** Python · Selenium 4 · pytest · Page Object Model · GitHub Actions
