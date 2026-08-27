from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base import BasePage as AbstractPage
import time

class BasePage(AbstractPage):
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def goto(self, url):
        self.driver.get(url)
        return self

    def take_screenshot(self, name: str): pass

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        self.find(locator).click()
        return self

    def fill_text(self, locator, text):
        element = self.find(locator)
        element.clear()
        element.send_keys(text)
        return self

    def upload_file(self, locator, file_path):
        element = self.find(locator)
        element.send_keys(file_path)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def get_texts(self, locator, retries=3):
        """
        Возвращает список текстов всех элементов, соответствующих локатору.
        Если возникает StaleElementReferenceException, делает повторные попытки.
        """
        for attempt in range(retries):
            try:
                elements = self.find_all(locator)
                return [el.text for el in elements]
            except StaleElementReferenceException:
                if attempt == retries - 1:
                    raise
                time.sleep(0.5)  # небольшая пауза перед повторной попыткой
        return []

    def get_element_text(self, locator):
        return self.find(locator).text

    def is_element_disabled(self, locator) -> bool:
        element = self.find(locator)
        return element.get_attribute("disabled") is not None

    def wait_for_url_contains(self, partial_url: str):
        self.wait.until(EC.url_contains(partial_url))

    def is_element_visible(self, locator) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    def is_text_present_in_element(self, locator, text):
        try:
            self.wait.until(
            EC.text_to_be_present_in_element(locator, text)
            )
            return True
        except TimeoutException:
            return False