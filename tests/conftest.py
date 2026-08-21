import pytest
from faker import Faker
from playwright.sync_api import Page, expect

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

        page.get_by_role("link", name="Войти").click()
        page.locator("input[type=\"email\"]").fill(email)
        page.locator("input[type=\"password\"]").fill(password)
        page.get_by_role("button", name="Войти").click()

        expect(page).to_have_url("https://archiscope.ru/", timeout=10000)
        return page

    return __login