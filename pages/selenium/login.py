import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.selenium.base import BasePage

class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.email_input = (By.CSS_SELECTOR, "input[type='email']")
        self.password_input = (By.CSS_SELECTOR, "input[type='password']")

        self.login_button = (By.XPATH, "//button[text()='Войти']")

    def fill_email(self, email: str):
        self.fill_text(self.email_input, email)
        return self

    @allure.step("Заполнение поля ввода password")
    def fill_password(self, password: str):
        self.fill_text(self.password_input, password)
        return self

    @allure.step("Заполнение поля ввода email")
    def click_login(self):
        self.click(self.login_button)
        return self

    def redirect(self):
        try:
            self.wait.until(EC.url_to_be("https://archiscope.ru/"))
            from pages.selenium import MainPage
            return MainPage(self.driver)
        except TimeoutException:
            return self

    @allure.step("Заполнение формы и нажатие на кнопку 'Войти'")
    def login(self, email: str, password: str):
        self.fill_email(email).fill_password(password).click_login()
        return self.redirect()