import pytest
from faker import Faker
from playwright.sync_api import Page

@pytest.fixture(scope="session")
def fake():
    return Faker('ru_RU')

@pytest.fixture(scope="function")
def login(page: Page):
    page.goto("https://archiscope.ru/")

    page.get_by_role("link", name="Войти").click()
    page.locator("input[type=\"email\"]").fill("test@example.com")
    page.locator("input[type=\"password\"]").fill("password123")
    page.get_by_role("button", name="Войти").click()

    return page