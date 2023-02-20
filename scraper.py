from selenium.webdriver import Chrome

class Scraper:
    def __init__(self, browser: Chrome):
        self.browser = browser