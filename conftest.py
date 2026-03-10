import os                                          # used to read environment variables (e.g. CI=true on GitHub Actions)
import pytest                                       # pytest is the testing framework — needed for the @pytest.fixture decorator
from selenium import webdriver                      # webdriver is the Selenium module that controls the browser
from selenium.webdriver.chrome.service import Service   # Service tells Selenium where the ChromeDriver executable is
from webdriver_manager.chrome import ChromeDriverManager  # automatically downloads the correct ChromeDriver version


@pytest.fixture                                    # marks this function as a fixture — pytest will inject it into any test that requests 'driver'
def driver():
    service = Service(ChromeDriverManager().install())  # download (or reuse cached) ChromeDriver and create a Service object pointing to it

    options = webdriver.ChromeOptions()            # create a ChromeOptions object to configure browser behaviour before launch

    if os.getenv("CI"):                            # os.getenv("CI") reads the CI environment variable — GitHub Actions sets it to "true" automatically
        options.add_argument("--headless")         # run Chrome with no visible window — required on CI servers that have no monitor
        options.add_argument("--no-sandbox")       # disable Chrome's security sandbox — required on Linux CI which often runs as root
        options.add_argument("--disable-dev-shm-usage")  # use /tmp instead of /dev/shm for memory — CI containers have very limited shared memory
        options.add_argument("--window-size=1920,1080")  # set a fixed viewport — headless Chrome defaults to a tiny size that can hide elements

    driver = webdriver.Chrome(service=service, options=options)  # launch Chrome with the configured service and options
    yield driver                                   # hand the driver to the test — everything before yield is setup, everything after is teardown
    driver.quit()                                  # close the browser and end the ChromeDriver process after the test finishes
