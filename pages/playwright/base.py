import allure
from pages.base import BasePage as AbstractPage

class BasePage(AbstractPage):
    def __init__(self, page):
        self.page = page

    @allure.step("Переход на конкретную страницу")
    def goto(self, url):
        with allure.step(f"Переход на страницу {url}"):
            self.page.goto(url)

        return self
