
class MainPage:
    def __init__(self, page):
        self.page = page

        self.create_news_btn = page.locator("a[href='/news/create']")
        self.login_button = page.get_by_role("link", name="Войти")
        self.register_button = page.get_by_role("link", name="Регистрация")

        self.next_button = page.get_by_role("button", name="»")
        self.prev_button = page.get_by_role("button", name="«")

        self.avatar = page.locator("[role='button'].avatar")
        self.profile_button = page.get_by_role("link", name="Профиль")

        self.news_titles = page.locator(".card-title a")
        self.active_page = page.locator(".join .btn-primary")
        self.page_buttons = page.locator(".join .btn:not(.btn-disabled):not(:has-text('«')):not(:has-text('»'))")

    def get_page(self, number: int):
        return self.page.locator(f".join .btn:has-text(\"{number}\")")

    def get_active_page_number(self) -> str:
        return self.active_page.text_content()

    def get_by_title(self, title):
        return self.page.get_by_text(title)