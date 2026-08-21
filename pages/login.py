
class LoginPage():
    def __init__(self, page):
        self.page = page
        self.email_input = page.locator("input[type=\"email\"]")
        self.password_input = page.locator("input[type=\"password\"]")
        self.login_button = page.get_by_role("button", name="Войти")