import pytest
import allure
from helpers import generate_user
from tests.conftest import BASE_URL
from pages.selenium import MainPage, LoginPage, RegisterPage

@allure.epic("Регистрация")
@allure.feature("Регистрация")
class TestRegister:
    @allure.story("Позитивный тест")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("""
    1 Перейти на главную страницу сайта
    2 Сгенерировать данные пользователя
    3 Заполнить форму регистрации
    4 Заполнить форму логина
    5 Проверить успешных вход
    """)
    def test_register_success(self, main_page, fake):
        user = generate_user(fake)

        register_page = main_page.goto_register()
        register_page.fill_form(**user).reg_confirm()

        login_page = register_page.register_status()
        assert isinstance(login_page, LoginPage)

        main_page = login_page.login(user["email"], user["password"])
        assert isinstance(main_page, MainPage)

    @allure.epic("Регистрация")
    @allure.feature("Регистрация")
    @allure.story("Негативный сценарий регистрации")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("""
    1 Перейти на главную страницу сайта
    2 Сгенерировать данные пользователя
    3 Заполнить форму регистрации
    4 Заполнить форму логина
    5 Проверить успешных вход
    """)
    def test_register_fail(self, main_page, fake):
        with allure.step("Регистрируем пользователя"):
            user = generate_user(fake)

            register_page = main_page.goto_register()
            register_page.fill_form(**user).reg_confirm()
        with allure.step("Возвращаемся на страницу регистрации"):
            register_page.goto(f"{BASE_URL}/register")

        with allure.step("Пытаемся заново зарегистрироваться с этими же данными"):
            register_page = main_page.goto_register()
            register_page.fill_form(**user).reg_confirm()

            register_page = register_page.register_status()
            assert isinstance(register_page, RegisterPage)



