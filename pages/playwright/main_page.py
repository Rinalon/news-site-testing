import allure
from playwright.sync_api import expect
from pages.playwright.base import BasePage

class MainPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
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

    @allure.step("Получение страницы по её номеру")
    def get_page(self, number: int) -> "Locator":
        return self.page.locator(f".join .btn:has-text(\"{number}\")")

    @allure.step("Получение номера активной страницы")
    def get_active_page_number(self) -> str:
        return self.active_page.text_content()

    @allure.step("Поиск новости по заголовку")
    def get_by_title(self, title: str) -> "Locator":
        return self.page.get_by_text(title)

    @allure.step("Переход к странице логина")
    def goto_login(self) -> "LoginPage":
        self.login_button.click()
        expect(self.page).to_have_url(f"{self.BASE_URL}login", timeout=10000)

        from pages.playwright.login import LoginPage
        return LoginPage(self.page)

    @allure.step("Переход к странице регистрации")
    def goto_register(self) -> "RegisterPage":
        self.register_button.click()
        expect(self.page).to_have_url(f"{self.BASE_URL}register", timeout=10000)

        from pages.playwright.register import RegisterPage
        return RegisterPage(self.page)

    @allure.step("Переход к странице профиля")
    def goto_profile(self) -> "UserProfilePage":
        self.avatar.click()
        self.profile_button.click()
        expect(self.page).to_have_url(f"{self.BASE_URL}profile", timeout=10000)

        from pages.playwright.user_profile import UserProfilePage
        return UserProfilePage(self.page)

    @allure.step("Переход к странице создания новости")
    def goto_create_news(self) -> "NewsCreatingPage":
        self.create_news_btn.click()
        expect(self.page).to_have_url(f"{self.BASE_URL}news/create", timeout=10000)

        from pages.playwright.news_creating import NewsCreatingPage
        return NewsCreatingPage(self.page)