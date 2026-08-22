import pytest
from playwright.sync_api import Page
from helpers import generate_user
from pages import RegisterPage, MainPage, LoginPage


def test_registration(page: Page, faker):
    main_page = MainPage(page).goto("https://archiscope.ru/")

    user = generate_user(faker)

    register_page = RegisterPage(main_page.goto_register())

    page = register_page.fill_form(**user)
    login_page = LoginPage(page)

    login_page.login(user["email"], user["password"])