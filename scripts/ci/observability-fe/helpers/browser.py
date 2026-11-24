import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.service import Service

def create_chrome_driver(headless: bool) -> WebDriver:

    """Create and return a configured Chrome WebDriver instance"""
    # Initialize Chrome options.
    options = Options()

    # Configure headless mode if requested.
    if headless:
        options.add_argument("--headless")

    # Set default window size and enable BiDi support.
    options.add_argument("--window-size=1920,1080")
    options.enable_bidi = True

    # Use explicit browser binary when provided (CI).
    chrome_bin = os.getenv("CHROME_BIN")
    if chrome_bin:
        options.binary_location = chrome_bin

    # Use explicit ChromeDriver binary when provided (CI).
    chromedriver_bin = os.getenv("CHROMEDRIVER_BIN")
    service = Service(executable_path=chromedriver_bin) if chromedriver_bin else Service()

    # Create the Chrome WebDriver with the specified service and options.
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(30)

    return driver