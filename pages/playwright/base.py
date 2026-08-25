from pages.base import BasePage as AbstractPage

class BasePage(AbstractPage):
    def __init__(self, page):
        self.page = page

    def goto(self, url):
        self.page.goto(url)
        return self