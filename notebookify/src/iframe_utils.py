from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import logging

logger = logging.getLogger(__name__)


def capture_iframe_snapshot(
    url, output_path, chromedriver_path="path/to/chromedriver"
):
    """
    Capture a snapshot of an iframe from a given URL using Selenium.
    """
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        service = Service(chromedriver_path)

        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(url)
        time.sleep(3)  # Wait for the iframe to load

        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)

        driver.save_screenshot(output_path)
        logger.info(f"Snapshot saved to {output_path}")

        driver.quit()
    except Exception as e:
        logger.error(f"Error capturing iframe snapshot: {e}")
