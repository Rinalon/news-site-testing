import pytest
from faker import Faker


@pytest.fixture(scope="session")
def fake():
    return Faker('ru_RU')

USERS = [
        {"email": "test@example.com", "password": "password123"},
        {"email": "example@example.com", "password": "123pass456"},
]

