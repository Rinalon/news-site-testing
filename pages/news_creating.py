
class NewsCreatingPage:
    def __init__(self, page):
        self.page = page
        self.title_input = page.locator("input[name=\"title\"]")
        self.subtitle_input = page.locator("input[name=\"subtitle\"]")
        self.text_input = page.locator("textarea[name=\"text\"]")
        self.tags_input = page.locator("input[name=\"tags\"]")
        self.img_load = page.locator("input[type=\"file\"]")
        
        self.submit_button = page.locator("button[type=\"submit\"]")