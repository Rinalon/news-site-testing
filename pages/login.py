from playwright.sync_api import expect
from pages.base import BasePage

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

        self.email_input = page.locator("input[type=\"email\"]")
        self.password_input = page.locator("input[type=\"password\"]")
        self.login_button = page.get_by_role("button", name="Войти")

    def fill_email(self, email):
        self.email_input.fill(email)
        return self

    def fill_password(self, password):
        self.password_input.fill(password)
        return self

    def click_login(self):
        self.login_button.click()
        return self

    def login(self, email, password):
        self.fill_email(email).fill_password(password).click_login()
        expect(self.page).to_have_url("https://archiscope.ru/", timeout=10000)
        return self.page