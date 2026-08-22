import pytest
from playwright.sync_api import Page
from helpers import generate_user
from pages import RegisterPage, MainPage, LoginPage


def test_registration(page: Page, faker):
    main_page = MainPage(page).goto("https://archiscope.ru/")

    user = generate_user(faker)

    register_page = RegisterPage(main_page.goto_register())

    # Заполнение формы Регистрации
    register_page.first_name_input.fill(user["first_name"])
    register_page.last_name_input.fill(user["last_name"])
    register_page.email_input.fill(user["email"])
    register_page.phone_input.fill(user["phone"])
    register_page.password_input.fill(user["password"])

    register_page.reg_button.click()

    login_page = LoginPage(register_page.page)

    # Заполнение формы Логина
    login_page.email_input.fill(user["email"])
    login_page.password_input.fill(user["password"])

    login_page.login_button.click()

"""

"""