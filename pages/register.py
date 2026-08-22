import re
from playwright.sync_api import expect
from pages.base import BasePage

class RegisterPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.first_name_input = page.locator("input[name=\"first_name\"]")
        self.last_name_input = page.locator("input[name=\"last_name\"]")
        self.email_input = page.locator("input[type=\"email\"]")
        self.phone_input = page.locator("input[name=\"phone\"]")
        self.password_input = page.locator("input[name=\"password\"]")
        self.reg_button = page.get_by_role("button", name="Зарегистрироваться")

        self.alert_message = page.get_by_text(re.compile(r"already registered$"))

    def fill_form(
            self,
            first_name: str,
            last_name: str,
            email: str,
            phone: str,
            password: str,
    ):
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.email_input.fill(email)
        self.phone_input.fill(phone)
        self.password_input.fill(password)

        self.reg_button.click()
        expect(self.page).to_have_url("https://archiscope.ru/login", timeout=10000)
        return self.page
