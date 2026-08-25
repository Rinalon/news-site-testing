from faker import Faker
from pygments.lexers import data
from datetime import datetime


def generate_user(faker: Faker, exclude: tuple[str] | None = None) -> dict:
    now = datetime.now().strftime("%Y%m%d_%H%M%S")

    data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": f"test_{now}_{faker.email()}",
        "phone": faker.phone_number(),
        "password": faker.password(length=10, special_chars=True, digits=True),
    }

    if exclude:
        for key in exclude:
            data.pop(key, None)
    return data