# Selenium POM — QA Automation Portfolio

![Tests](https://github.com/ahmedhesham2020/selenium-pom/actions/workflows/tests.yml/badge.svg)

End-to-end UI automation framework for [SauceDemo](https://www.saucedemo.com) using Selenium WebDriver and the Page Object Model pattern.

## Skills Demonstrated

| Skill | Where |
|-------|-------|
| Page Object Model (POM) | `pages/` — one class per page |
| Explicit waits (`WebDriverWait` + `EC`) | All page classes |
| JavaScript click (macOS/Chrome compatibility) | `inventory_page.py`, `cart_page.py`, `checkout_page.py` |
| React controlled input handling | `checkout_page.py` → `_react_input()` |
| Fixture-based driver setup/teardown | `tests/` → `driver` fixture |
| Custom markers: smoke + regression | `pytest.ini` + test files |
| GitHub Actions CI/CD | `.github/workflows/tests.yml` |
| HTML test reports | `pytest.ini` → `--html=report.html` |

## Project Structure

```
selenium-pom/
├── conftest.py               # empty root marker
├── pytest.ini                # config: markers, HTML report, testpaths
├── requirements.txt
├── pages/
│   ├── login_page.py         # locators + actions for login page
│   ├── inventory_page.py     # locators + actions for inventory page
│   ├── cart_page.py          # locators + actions for cart page
│   └── checkout_page.py      # locators + actions for checkout pages
└── tests/
    ├── test_login.py         # login success, invalid login, item count
    └── test_checkout.py      # add to cart, full checkout flow
```

## Test Coverage

| File | Tests | Markers |
|------|-------|---------|
| `test_login.py` | 3 | smoke |
| `test_checkout.py` | 2 | regression |
| **Total** | **5** | |

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
```

## User Flow Covered

```
Login → Add item to cart → Go to cart → Checkout
     → Fill shipping info → Confirm order → Verify completion
```

---

**Author:** Ahmed Hesham — SW Validation Engineer → QA Automation Engineer
**Stack:** Python · Selenium 4 · pytest · Page Object Model · GitHub Actions
