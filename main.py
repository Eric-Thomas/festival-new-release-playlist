import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scraper import Scraper


def handler(event, context):
    main()


def main():
    try:
        browser = get_chrome_browser()
        scraper = Scraper(browser)
        releases = scraper.scrape_new_releases()
    finally:
        browser.quit()


def get_chrome_browser() -> webdriver.Chrome:
    # Get driver based on runtime environment
    if (
        os.environ.get("RUNTIME_ENV") != None
        and os.environ.get("RUNTIME_ENV").lower() == "prod"
    ):  # Prod driver is packed into lambda layer
        options = Options()
        options.binary_location = "/opt/headless-chromium"
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        return webdriver.Chrome("/opt/chromedriver", options=options)
    else:
        # Local chrome dirver for development. Should be named 'chromedriver'
        return webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"))


if __name__ == "__main__":
    main()
