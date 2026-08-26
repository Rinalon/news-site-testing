import allure
import pytest
import logging
from faker import Faker
from pathlib import Path

BASE_URL = "https://archiscope.ru/"

ARTIFACTS_DIR = Path(__file__).parent.parent / "artifacts"
TRACES_DIR = ARTIFACTS_DIR / "tracers"
SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
VIDEOS_DIR = ARTIFACTS_DIR / "videos"

logger = logging.getLogger(__name__)

for directory in [ARTIFACTS_DIR, TRACES_DIR, SCREENSHOTS_DIR, VIDEOS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Данные тестовых пользователей
USERS = [
        {"email": "test@example.com", "password": "password123"},
        {"email": "example@example.com", "password": "123pass456"},
]

@pytest.fixture(scope="session")
def fake() -> Faker:
    """Фикстура, предоставляющая экземпляр Faker для генерации тестовых данных."""
    return Faker('ru_RU')

@pytest.fixture(scope="function", autouse=True)
def allure_setup(request):
    test_name = request.node.name.replace("test_", "").replace("_", " ").title()
    allure.dynamic.title(test_name)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для сохранения статуса выполнения теста."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)