import pytest
from helpers.browser import create_chrome_driver

@pytest.fixture
def browser():
    driver = create_chrome_driver(headless=True)
    
    yield driver
    driver.quit()