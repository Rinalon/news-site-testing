from pages.base import BasePage

class NewsPage(BasePage):
    def get_heading(self, name, lvl):
        return self.page.get_by_role("heading", name=name, level=lvl)

    def get_text(self, text):
        return self.page.get_by_text(text)

    def get_tag(self, name):
        return self.page.locator(f"span:has-text(\"{name}\")")

    def get_img_by_alt(self, alt):
        return self.page.locator(f"img[alt=\"{alt}\"]")