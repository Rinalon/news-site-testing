import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.selenium.base import BasePage

class CreateNewsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)


        self.title_input = (By.CSS_SELECTOR, "input[name='title']")
        self.subtitle_input = (By.CSS_SELECTOR, "input[name='subtitle']")
        self.text_input = (By.CSS_SELECTOR, "textarea[name='text']")
        self.tags_input = (By.CSS_SELECTOR, "input[name='tags']")
        self.img_load = (By.CSS_SELECTOR, "input[type='file']")
        self.submit_button = (By.CSS_SELECTOR, "button[type='submit']")

    @allure.step("Заполнение заголовка")
    def fill_title(self, title: str):
        self.fill_text(self.title_input, title)
        return self

    @allure.step("Заполнение подзаголовка")
    def fill_subtitle(self, subtitle: str):
        self.fill_text(self.subtitle_input, subtitle)
        return self

    @allure.step("Заполнение текста")
    def fill_news_text(self, text: str):
        self.fill_text(self.text_input, text)
        return self

    @allure.step("Заполнение тегов")
    def fill_tags(self, tags: str):
        self.fill_text(self.tags_input, tags)
        return self

    @allure.step("Загрузка картинки")
    def load_image(self, image_path: str):
        self.upload_file(self.img_load, image_path)
        return self

    def submit(self):
        self.click(self.submit_button)
        return self

    def redirect(self):
        try:
            self.wait.until(EC.url_to_be(self.BASE_URL))
            from pages.selenium import MainPage
            return MainPage(self.driver)
        except TimeoutException:
            return self


    @allure.step("Заполнение формы создания новости")
    def fill_form(
        self,
        title: str = "",
        subtitle: str = "",
        text: str = "",
        tags: str = "",
        image: str = None,
    ):

        self.fill_title(title)
        self.fill_subtitle(subtitle)
        self.fill_news_text(text)
        self.fill_tags(tags)

        if image:
            self.load_image(image)

        return self