import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def driver():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    if os.getenv("CI"):                              # GitHub Actions sets CI=true automatically
        options.add_argument("--headless")           # no display on CI server
        options.add_argument("--no-sandbox")         # required on Linux CI
        options.add_argument("--disable-dev-shm-usage")  # prevents memory crashes on CI
        options.add_argument("--window-size=1920,1080")  # consistent viewport
    driver = webdriver.Chrome(service=service, options=options)
    yield driver
    driver.quit()
