import allure
import pytest
from helpers import generate_user
from playwright.sync_api import expect
from pages.playwright import MainPage, LoginPage
from tests.conftest import BASE_URL

@allure.epic("Registration")
@allure.feature("Регистрация")
class TestRegister:

    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.main_page = MainPage(page).goto(BASE_URL)

    @allure.story("Позитивный тест")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("""
        1 Перейти на главную страницу сайта
        2 Сгенерировать данные пользователя
        3 Заполнить форму регистрации
        4 Нажать кнопку 'Зарегистрироваться'
        5 Заполнить форму логина
        6 Нажать кнопку 'Войти'
        7 Проверить успешных вход
    """)
    @pytest.mark.flaky # как-то раз упал при попытке регистрации. Вероятно был одновременный запрос на регистрацию
    def test_register_success(self, fake):
        user = generate_user(fake)

        register_page = self.main_page.goto_register()
        register_page.fill_form(**user).reg_confirm()

        login_page = register_page.redirect()

        assert isinstance(login_page, LoginPage), "Не удалось создать пользователя"
        login_page.login(user["email"], user["password"])

        main_page = login_page.redirect()
        assert isinstance(main_page, MainPage), "Ошибка логина под новым пользователем"

    @allure.story("Негативный тест")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("""
        1 Перейти на главную страницу сайта
        2 Сгенерировать данные пользователя
        3 Заполнить форму регистрации
        4 Нажать кнопку 'Зарегистрироваться'
        5 Вернуться на главную страницу сайта 
        6 Заполнить форму с теми же данными
        7 Нажать кнопку 'Зарегистрироваться'
        8 Проверить наличие сообщения о том, что такой пользователь уже существует
    """)
    def test_register_fail(self, fake):
        user = generate_user(fake)

        register_page = self.main_page.goto_register()
        with allure.step("Заполняем и отправляем форму регистрации"):
            register_page.fill_form(**user).reg_confirm()

        with allure.step("Возвращаемся на страницу регистрации"):
            register_page.goto(f"{BASE_URL}/register")

        with allure.step("Пытаемся заново зарегистрироваться с этими же данными"):
            register_page = self.main_page.goto_register()
            register_page.fill_form(**user).reg_confirm()

        with allure.step("Проверим наличие сообщения об ошибке"):
            expect(register_page.alert_message).to_be_visible()