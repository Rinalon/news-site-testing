import allure
import pytest
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tests.conftest import logger, TRACES_DIR, SCREENSHOTS_DIR, BASE_URL
from pages.selenium import MainPage, LoginPage

@pytest.fixture(scope="session")
def browser():
    """
    Фикстура, создающая экземпляр драйвера Chrome на всю сессию тестов.

    Драйвер запускается с заданными опциями (размер окна, язык и т.д.).
    Для визуальной отладки headless отключён (можно включить через переменную окружения).

    Yields:
        WebDriver: Экземпляр драйвера для использования в тестах.

    Note:
        Драйвер автоматически закрывается после завершения всех тестов.
    """
    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=ru-RU")

    chrome_loc = Path(__file__).parent.parent.parent / "chrome-win64/chrome.exe"
    options.binary_location = str(chrome_loc)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_page_load_timeout(10)
    driver.implicitly_wait(5)

    yield driver

    driver.quit()


@pytest.fixture(scope="function")
def context(browser, request):
    """
        Фикстура, подготавливающая драйвер для каждого теста.

        Очищает cookies и localStorage между тестами для изоляции данных.
        Сохраняет информацию о тесте для обработки результатов.

        Args:
            browser: Фикстура браузера (session).
            request: Объект запроса pytest.

        Yields:
            WebDriver: Драйвер с очищенным состоянием.
    """
    test_name = request.node.name

    browser.delete_all_cookies()
    try:
        browser.execute_script("localStorage.clear();")
    except Exception: pass

    browser._test_name = test_name
    browser._test_failed = False

    yield browser

    if  hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        browser._test_failed = True

        screenshot_path = SCREENSHOTS_DIR / f"{test_name}.png"
        browser.save_screenshot(str(screenshot_path))
        allure.attach.file(str(screenshot_path), "Screenshot", attachment_type="image/png")
        logger.info(f"Скриншот сохранён: {screenshot_path}")

        log_path = TRACES_DIR / f"{test_name}.log"
        logs = browser.get_log("browser")
        if logs:
            with open(log_path, "w", encoding="utf-8") as f:
                for entry in logs:
                    f.write(f"{entry}\n")
            allure.attach.file(str(log_path), "Browser logs", attachment_type="text/plain")

@pytest.fixture(scope="function")
def main_page(context):
    with allure.step("Переход на главную страницу"):
        return MainPage(context).goto(BASE_URL)

@pytest.fixture(scope="function")
def login(main_page, context):
    """
    Фикстура-фабрика для авторизации пользователя.

    Использует драйвер из фикстуры context.

    Returns:
        callable: Функция вида (email: str, password: str) -> MainPage.
    """

    def __login(email: str, password: str) -> MainPage:
        with allure.step(f"Авторизация пользователя {email}"):
            try:
                with allure.step("Переход на страницу логина"):
                    login_page = main_page.goto_login()

                with allure.step("Ввод учетных данных и вход"):
                    result_page = login_page.login(email, password)

                if isinstance(result_page, MainPage):
                    logger.info("Успешный логин")
                    return result_page
                else:
                    raise ValueError(f"Не вышло залогиниться под следующими параметрами: {'\n' + email + '\n' + password}')")

            except Exception as e:
                logger.error(f"Ошибка логина: {e}")
                allure.attach(
                    context.get_screenshot_as_png(),
                    name="login_error",
                    attachment_type=allure.attachment_type.PNG
                )
                raise e

    return __login