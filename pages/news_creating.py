import allure
from pages.base import BasePage

class NewsCreatingPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.title_input = page.locator("input[name=\"title\"]")
        self.subtitle_input = page.locator("input[name=\"subtitle\"]")
        self.text_input = page.locator("textarea[name=\"text\"]")
        self.tags_input = page.locator("input[name=\"tags\"]")
        self.img_load = page.locator("input[type=\"file\"]")
        
        self.submit_button = page.locator("button[type=\"submit\"]")

    @allure.step("Заполнение заголовка")
    def fill_title(self, title):
        self.title_input.fill(title)
        return self

    @allure.step("Заполнение подзаголовка")
    def fill_subtitle(self, subtitle):
        self.subtitle_input.fill(subtitle)
        return self

    @allure.step("Заполнение текста")
    def fill_text(self, text):
        self.text_input.fill(text)
        return self

    @allure.step("Заполнение тегов")
    def fill_tags(self, tags):
        self.tags_input.fill(tags)
        return self

    @allure.step("Загрузка картинки")
    def load_image(self, img):
        self.img_load.set_input_files(img)

    @allure.step("Заполнение формы создания новости")
    def fill_form(
            self,
            title: str | None = "",
            subtitle: str | None = "",
            text: str | None = "",
            tags: str | None = "",
            image: str | None = None,
    ):
        self.fill_title(title)
        self.fill_subtitle(subtitle)
        self.fill_text(text)
        self.fill_tags(tags)

        if image:
            self.load_image(image)

        self.submit_button.click()
        return self.page
