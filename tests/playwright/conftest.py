import pytest
from playwright.sync_api import Page
from pages import MainPage, LoginPage

@pytest.fixture(scope="function")
def login(page: Page):
    def __login(email, password):
        main_page = MainPage(page).goto("https://archiscope.ru/")
        login_page = LoginPage(main_page.goto_login())

        return MainPage(login_page.login(email, password))

    return __login