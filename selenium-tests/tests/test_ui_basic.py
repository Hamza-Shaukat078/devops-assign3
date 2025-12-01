import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


# Jenkins will inject this as http://web:5000 (see Jenkinsfile)
APP_URL = os.environ.get("APP_URL", "http://web:5000")


def create_driver():
    """
    Create a headless Chromium WebDriver.
    This expects:
      - chromium      at /usr/bin/chromium
      - chromedriver  at /usr/bin/chromedriver
    (installed in the Dockerfile)
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Paths for Debian-based chromium/chromedriver
    chrome_options.binary_location = "/usr/bin/chromium"
    service = Service("/usr/bin/chromedriver")

    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def test_homepage_loads():
    """
    Basic smoke test:
    - Open the app home page using APP_URL (injected by Jenkins)
    - Assert that we got a valid HTML page.
    """
    driver = create_driver()
    try:
        driver.get(APP_URL)
        time.sleep(2)  # small wait for render

        page_source = driver.page_source.lower()
        assert "<html" in page_source
        assert "</html>" in page_source
    finally:
        driver.quit()


def test_page_has_title():
    """
    Validate that the page has a non-empty title.
    """
    driver = create_driver()
    try:
        driver.get(APP_URL)
        time.sleep(2)

        title = driver.title
        assert isinstance(title, str)
        assert title.strip() != ""
    finally:
        driver.quit()
