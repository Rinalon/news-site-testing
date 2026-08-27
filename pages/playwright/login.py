import allure
from playwright.sync_api import expect
from pages.playwright.base import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.email_input = page.locator("input[type=\"email\"]")
        self.password_input = page.locator("input[type=\"password\"]")
        self.login_button = page.get_by_role("button", name="Войти")

    @allure.step("Заполнение поля ввода email")
    def fill_email(self, email: str):
        self.email_input.fill(email)
        return self

    @allure.step("Заполнение поля ввода password")
    def fill_password(self, password: str):
        self.password_input.fill(password)
        return self

    @allure.step("Заполнение поля ввода email")
    def click_login(self):
        self.login_button.click()
        return self

    @allure.step("Проверка перехода")
    def redirect(self):
        try:
            expect(self.page).to_have_url(self.BASE_URL, timeout=10000)

            from pages.playwright.main_page import MainPage
            return MainPage(self.page)
        except AssertionError:
            return self

    @allure.step("Заполнение формы и нажатие на кнопку 'Войти'")
    def login(self, email: str, password: str):
        self.fill_email(email).fill_password(password).click_login()

        return self