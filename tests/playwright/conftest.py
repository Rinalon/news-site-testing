import pytest
from playwright.sync_api import Page, Browser, BrowserContext
from pages.playwright import MainPage, LoginPage

@pytest.fixture(scope="session")
def browser():
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser):
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        locale="ru-RU",
    )
    context.tracing.start(screenshots=True, snapshots=True)

    yield context

    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    page = context.new_page()

    yield page

    page.close()

@pytest.fixture(scope="function")
def login(page) -> MainPage:
    def __login(email: str, password: str) -> MainPage:
        main_page = MainPage(page).goto("https://archiscope.ru/")
        login_page = LoginPage(main_page.goto_login())

        return MainPage(login_page.login(email, password))

    return __login