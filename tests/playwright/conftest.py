import allure
import pytest
from tests.conftest import logger, BASE_URL, VIDEOS_DIR, TRACES_DIR, SCREENSHOTS_DIR
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
def context(browser: Browser, request):
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
    test_name = request.node.name

    context = browser.new_context(
        locale="ru-RU",
        record_video_dir=str(VIDEOS_DIR)
    )
    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    context._test_name = test_name
    context._test_failed = False

    yield context

    if context._test_failed:
        trace_path = TRACES_DIR / f"{test_name}.zip"
        context.tracing.stop(path=str(trace_path))
        allure.attach.file(str(trace_path), "Playwright trace", attachment_type="application/zip")

        logger.info(f"Результат теста {test_name} сохранён")
    else:
        context.tracing.stop()

    video_path = VIDEOS_DIR / f"{test_name}.webm"
    if context._test_failed and video_path.exists():
        allure.attach.file(str(video_path), "Video", attachment_type="video/webm",)
    elif video_path.exists():
        video_path.unlink()

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
    page.set_default_timeout(10000)

    yield page

    if request.node.rep_call.failed:
        context._test_failed = True

        screenshot_path = SCREENSHOTS_DIR / f"{request.node.name}.png"
        page.screenshot(path=str(screenshot_path), full_page=True)

        allure.attach.file(str(screenshot_path), "Screenshot", attachment_type="image/png")
        logger.info(f"Скриншот сохранён: {screenshot_path}")

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

                logger.info("Успешный логин")
                return result_page

            except Exception as e:
                logger.error(f"Ошибка логина: {e}")
                allure.attach(
                    page.screenshot(),
                    name="login_error",
                    attachment_type=allure.attachment_type.PNG
                )
                raise e

    return __login