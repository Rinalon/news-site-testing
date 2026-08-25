import allure
import pytest
from helpers import generate_user
from pages.playwright import RegisterPage, MainPage, LoginPage

@allure.epic("Registration")
@allure.feature("Регистрации")
@allure.story("Полный тест регистрации: от заполнения формы до логина под новым аккаунтом")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
1 Перейти на главную страницу сайта
2 Сгенерировать данные пользователя
3 Заполнить форму регистрации
4 Заполнить форму логина
5 Проверить успешных вход
""")
def test_registration(page, faker):
    main_page = MainPage(page).goto("https://archiscope.ru/")

    user = generate_user(faker)

    register_page = RegisterPage(main_page.goto_register())

    page = register_page.fill_form(**user)
    login_page = LoginPage(page)

    login_page.login(user["email"], user["password"])