import allure
from selenium.webdriver.common.by import By
from pages.selenium.base import BasePage

class NewsPage(BasePage):
    @allure.step("Получение заголовка по тексту и уровню")
    def get_heading(self, name: str, level: int) -> tuple:
        xpath = f"//h{level}[normalize-space(text())='{name}']"
        return (By.XPATH, xpath)

    @allure.step("Получение текста по содержанию")
    def get_text(self, text: str) -> tuple:
        xpath = f"//*[normalize-space(text())='{text}']"
        return (By.XPATH, xpath)

    @allure.step("Получение тега по содержанию")
    def get_tag(self, name: str) -> tuple:
        xpath = f"//span[contains(text(), '{name}')]"
        return (By.XPATH, xpath)

    @allure.step("Получение картинки по альтернативному тексту")
    def get_img_by_alt(self, alt: str) -> tuple:
        return (By.CSS_SELECTOR, f"img[alt='{alt}']")