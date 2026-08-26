import pytest
from faker import Faker

@pytest.fixture(scope="session")
def fake() -> Faker:
    """Фикстура, предоставляющая экземпляр Faker для генерации тестовых данных."""
    return Faker('ru_RU')

BASE_URL = "https://archiscope.ru/"

# Данные тестовых пользователей
USERS = [
        {"email": "test@example.com", "password": "password123"},
        {"email": "example@example.com", "password": "123pass456"},
]

