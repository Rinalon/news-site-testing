import pytest
from faker import Faker
from playwright.sync_api import Page, expect
from pages import MainPage, LoginPage

@pytest.fixture(scope="session")
def fake():
    return Faker('ru_RU')

USERS = [
        {"email": "test@example.com", "password": "password123"},
        {"email": "example@example.com", "password": "123pass456"},
]

@pytest.fixture(scope="function")
def login(page: Page):
    def __login(email, password):
        main_page = MainPage(page).goto("https://archiscope.ru/")
        login_page = LoginPage(main_page.goto_login())

        return MainPage(login_page.login(email, password))

    return __login