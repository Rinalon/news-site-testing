from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from pages.base import BasePage as AbstractPage

class BasePage(AbstractPage):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def goto(self, url):
        self.driver.get(url)
        return self