import allure
from pages.base import BasePage

class NewsPage(BasePage):
    @allure.step("Получение заголовка по тексту и уровню")
    def get_heading(self, name, lvl):
        return self.page.get_by_role("heading", name=name, level=lvl)

    @allure.step("Получение текста по содержанию")
    def get_text(self, text):
        return self.page.get_by_text(text)

    @allure.step("Получение тега по содержанию")
    def get_tag(self, name):
        return self.page.locator(f"span:has-text(\"{name}\")")

    @allure.step("Получение картинки по альтернативному тексту")
    def get_img_by_alt(self, alt):
        return self.page.locator(f"img[alt=\"{alt}\"]")