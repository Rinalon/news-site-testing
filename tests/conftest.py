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
        page.goto("https://archiscope.ru/")
        main_page = MainPage(page)
        main_page.login_button.click()

        login_page = LoginPage(main_page.page)

        login_page.email_input.fill(email)
        login_page.password_input.fill(password)
        login_page.login_button.click()

        expect(login_page.page).to_have_url("https://archiscope.ru/", timeout=10000)
        return MainPage(login_page.page)

    return __login