from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver

def create_chrome_driver(headless: bool) -> WebDriver:

    """Create and return a configured Chrome WebDriver instance"""
    options = Options()

    if headless:
        options.add_argument("--headless")

    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)

    return driver