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

    def fill_form(
            self,
            title: str | None = "",
            subtitle: str | None = "",
            text: str | None = "",
            tags: str | None = "",
            image: str | None = None,
    ):
        self.title_input.fill(title)
        self.subtitle_input.fill(subtitle)
        self.text_input.fill(text)
        self.tags_input.fill(tags)

        if image:
            self.img_load.set_input_files(image)

        self.submit_button.click()
        return self.page
