from faker import Faker
from pygments.lexers import data


def generate_user(faker: Faker, exclude: tuple[str] | None = None) -> dict:
    data = {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "phone": faker.phone_number(),
        "password": faker.password(length=10, special_chars=True, digits=True),
    }

    if exclude:
        for key in exclude:
            data.pop(key, None)
    return data