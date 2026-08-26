import allure
import pytest
from tests.conftest import BASE_URL
from playwright.sync_api import Browser, BrowserContext
from pages.playwright import MainPage, LoginPage

@pytest.fixture(scope="session")
def browser():
    """
        Фикстура, создающая экземпляр браузера Chromium на всю сессию тестов.

        Браузер запускается в видимом режиме для визуальной отладки.

        Yields:
            Browser: Экземпляр браузера Playwright для использования в тестах.

        Note:
            Браузер автоматически закрывается после завершения всех тестов.
    """
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()

@pytest.fixture(scope="function")
def context(browser: Browser):
    """
        Фикстура, создающая новый браузерный контекст для каждого теста.

        Контекст изолирует данные между тестами (cookies, localStorage).
        Включает:
        - Viewport 1920x1080
        - Русскую локаль (ru-RU)
        - Tracing (сбор скриншотов и снапшотов для отладки)

        Yields:
            BrowserContext: Контекст для использования в тесте.

        Note:
            Контекст автоматически закрывается после завершения теста.
    """
    context = browser.new_context(
        locale="ru-RU",
    )
    context.tracing.start(screenshots=True, snapshots=True)

    yield context

    context.close()

@pytest.fixture(scope="function")
def page(context: BrowserContext, request):
    """
        Фикстура, создающая новую страницу в текущем контексте.

        Yields:
            Page: Страница для использования в тесте.

        Note:
            Страница автоматически закрывается после завершения теста.
    """
    page = context.new_page()

    yield page

    page.close()

@pytest.fixture(scope="function")
def login(page) -> MainPage:
    """
        Фикстура-фабрика для авторизации пользователя
        Returns:
            callable: Функция вида (email: str, password: str) -> MainPage.
    """
    def __login(email: str, password: str) -> MainPage:
        with allure.step(f"Авторизация пользователя {email}"):
            try:
                main_page = MainPage(page).goto(BASE_URL)

                with allure.step("Переход на страницу логина"):
                    login_page = LoginPage(main_page.goto_login())

                with allure.step("Ввод учетных данных и вход"):
                    result_page = MainPage(login_page.login(email, password))
                return result_page

            except Exception as e:
                allure.attach(
                    page.screenshot(),
                    name="login_error",
                    attachment_type=allure.attachment_type.PNG
                )
                raise e

    return __login