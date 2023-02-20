import re
import time
from typing import List

from selenium.webdriver import Chrome
from bs4 import BeautifulSoup


class Scraper:

    METACRITIC_NEW_RELEASES_URL = (
        "https://www.metacritic.com/browse/albums/release-date/new-releases/date"
    )
    METACRITIC_BASE_URL = "https://www.metacritic.com"

    def __init__(self, browser: Chrome):
        self.browser = browser

    def scrape_new_releases(self):
        releases = []
        current_url = self.METACRITIC_NEW_RELEASES_URL
        while current_url:
            releases.append(self._scrape_page(current_url))
            next_url = self._get_next_url(current_url)
            current_url = next_url

        return releases

    def _get_next_url(self, url):
        self.browser.get(url)
        time.sleep(2)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        next = soup.find("a", rel="next")
        if next:
            return f"{self.METACRITIC_BASE_URL}{next.attrs.get('href')}"
        return None

    def _scrape_page(self, url):
        print(f"Scraping page {url}")
        self.browser.get(url)
        time.sleep(2)
        soup = BeautifulSoup(self.browser.page_source, "html.parser")
        container_divs = soup.find_all("div", class_="browse_list_wrapper")
        releases = []
        for container_div in container_divs:
            releases.append(self._get_releases(container_div))

        return releases

    def _get_releases(self, container_div) -> List:
        releases = []
        release_rows = container_div.find_all("tr")
        for release_row in release_rows:
            release_info = self._get_release_info(release_row)
            if release_info:
                releases.append(release_info)

        return releases

    def _get_release_info(self, release_row):
        # Ignore spacer rows
        if release_row.attrs.get("class") and "spacer" in release_row.attrs["class"]:
            return

        release_info = {}

        album_name = release_row.find("h3").text
        release_info["album_name"] = album_name

        artist_div = release_row.find("div", class_="artist")
        artist_name = artist_div.text.strip().split()[1]
        release_info["artist_name"] = artist_name

        release_date = release_row.find("span").text.strip()
        release_info["release_date"] = release_date

        print(release_info)

        return release_info
