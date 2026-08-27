import allure
from playwright.sync_api import expect
from pages.playwright.base import BasePage

class UserProfilePage(BasePage):
    """
        Page Object для страницы профиля пользователя.

        Предоставляет методы для взаимодействия с элементами страницы профиля:
        заполнение полей, нажатие кнопки "Сохранить"

        Attributes:
            first_name_input (Locator): Локатор поля с именем пользователя.
            last_name_input (Locator): Локатор поля с фамилией пользователя.
            phone_input (Locator): Локатор поля с номером телефона пользователя.
            email_input (Locator): Локатор поля с email пользователя.
            password_input (Locator): Локатор поля с паролем пользователя.
            save_button (Locator): Локатор кнопки сохранения изменений.
            access_message (Locator): Локатор сообщения о успешном изменении данных пользователя.

        Note:
            Все методы возвращают self для цепочки вызовов (fluent interface).
    """
    def __init__(self, page):
        super().__init__(page)

        self.first_name_input = page.locator("input[name='first_name']")
        self.last_name_input = page.locator("input[name='last_name']")
        self.phone_input = page.locator("input[name='phone']")
        self.email_input = page.locator("input[type='email']")
        self.password_input = page.locator("input[name='password']")

        self.save_button = page.get_by_role("button", name="Сохранить")

        self.access_message = page.get_by_text("Профиль обновлён")

    @allure.step("Заполнение поля ввода имени")
    def fill_first_name(self, first_name: str):
        self.first_name_input.fill(first_name)
        return self

    @allure.step("Заполнение поля ввода фамилии")
    def fill_last_name(self, last_name: str):
        self.last_name_input.fill(last_name)
        return self

    @allure.step("Заполнение поля ввода телефона")
    def fill_phone(self, phone):
        self.phone_input.fill(phone)
        return self

    @allure.step("Заполнение поля ввода email")
    def fill_email(self, email):
        self.email_input.fill(email)
        return self

    @allure.step("Заполнение поля ввода пароля")
    def fill_password(self, password):
        self.password_input.fill(password)
        return self

    @allure.step("Нажатие кнопки 'Сохранить'")
    def click_save_button(self):
        self.save_button.click()
        expect(self.access_message).to_be_visible()
        return self.page

