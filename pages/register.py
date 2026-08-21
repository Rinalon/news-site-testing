import re

class RegisterPage():
    def __init__(self, page):
        self.page = page
        self.first_name_input = page.locator("input[name=\"first_name\"]")
        self.last_name_input = page.locator("input[name=\"last_name\"]")
        self.email_input = page.locator("input[type=\"email\"]")
        self.phone_input = page.locator("input[name=\"phone\"]")
        self.password_input = page.locator("input[name=\"password\"]")
        self.reg_button = page.get_by_role("button", name="Зарегистрироваться")

        self.alert_message = page.get_by_text(re.compile(r"already registered$"))