import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = "https://www.saucedemo.com"

@pytest.fixture 
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver  = webdriver.Chrome(service=service , options=options)
    #driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def wait(driver):
    return WebDriverWait(driver, 10)

def test_saucedemo_title(driver):
    driver.get(URL)
    assert "Swag Labs" in driver.title

def test_saucedemo_login_visible(driver):
    driver.get(URL)
    assert driver.current_url == "https://www.saucedemo.com/"

def test_login_with_valid_user(driver):
    driver.get(URL)
    driver.find_element(By.ID,"user-name").send_keys("standard_user")
    driver.find_element(By.ID,"password").send_keys("secret_sauce")
    driver.find_element(By.ID,"login-button").click()
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"

def test_login_with_wrong_password(driver):
    driver.get(URL)
    driver.find_element(By.ID,"user-name").send_keys("standard_user")
    driver.find_element(By.ID,"password").send_keys("wrong_password")
    driver.find_element(By.ID,"login-button").click()

    error = driver.find_element(By.CSS_SELECTOR,"[data-test='error']")
    assert "Username and password do not match" in error.text

def test_login_success(driver, wait):
    driver.get(URL)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
    wait.until(EC.visibility_of_element_located((By.ID, "login-button"))).click()

    wait.until(EC.url_contains("inventory"))
    assert driver.current_url == "https://www.saucedemo.com/inventory.html"

def test_login_error_message(driver, wait):
    driver.get(URL)
    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("wrong_password")
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()
    error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
    assert "Username and password do not match" in error.text

