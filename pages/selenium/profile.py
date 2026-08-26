import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.selenium.base import BasePage


class ProfilePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.first_name_input = (By.CSS_SELECTOR, "input[name='first_name']")
        self.last_name_input = (By.CSS_SELECTOR, "input[name='last_name']")
        self.phone_input = (By.CSS_SELECTOR, "input[name='phone']")
        self.email_input = (By.CSS_SELECTOR, "input[type='email']")
        self.password_input = (By.CSS_SELECTOR, "input[name='password']")

        self.save_button = (By.XPATH, "//button[text()='Сохранить']")

        self.access_message = (By.XPATH, "//*[text()='Профиль обновлён']")

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

    @allure.step("Нажатие кнопки 'Сохранить'")
    def click_save_button(self):
        self.click(self.save_button)
        
        self.wait.until(EC.visibility_of_element_located(self.access_message))
        return self