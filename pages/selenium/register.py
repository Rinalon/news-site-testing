import allure
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pages.playwright import RegisterPage
from pages.selenium.base import BasePage
from pages.selenium.login import LoginPage


class RegisterPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.first_name_input = (By.CSS_SELECTOR, "input[name='first_name']")
        self.last_name_input = (By.CSS_SELECTOR, "input[name='last_name']")
        self.email_input = (By.CSS_SELECTOR, "input[type='email']")
        self.phone_input = (By.CSS_SELECTOR, "input[name='phone']")
        self.password_input = (By.CSS_SELECTOR, "input[name='password']")
        self.reg_button = (By.XPATH, "//button[text()='Зарегистрироваться']")

        self.alert_message = (By.XPATH, "//*[contains(text(), 'already registered')]")

    @allure.step("Заполнение поля ввода имени")
    def fill_first_name(self, first_name: str):
        self.fill_text(self.first_name_input, first_name)
        return self

    @allure.step("Заполнение поля ввода фамилии")
    def fill_last_name(self, last_name: str):
        self.fill_text(self.last_name_input, last_name)
        return self

    @allure.step("Заполнение поля ввода телефона")
    def fill_phone(self, phone: str):
        self.fill_text(self.phone_input, phone)
        return self

    @allure.step("Заполнение поля ввода email")
    def fill_email(self, email: str):
        self.fill_text(self.email_input, email)
        return self

    @allure.step("Заполнение поля ввода пароля")
    def fill_password(self, password: str):
        self.fill_text(self.password_input, password)
        return self

    @allure.step("Подтверждение регистрации")
    def reg_confirm(self):
        self.click(self.reg_button)
        return self

    @allure.step("Проверка успешности регистрации")
    def register_status(self) -> LoginPage | RegisterPage:
        try:
            self.wait_for_url_contains("/login")
            return LoginPage(self.driver)
        except TimeoutException:
            self.find(self.alert_message)
            return self

    @allure.step("Заполнение формы регистрации")
    def fill_form(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
    ):

        self.fill_first_name(first_name)
        self.fill_last_name(last_name)
        self.fill_email(email)
        self.fill_phone(phone)
        self.fill_password(password)

        return self