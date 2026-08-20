from faker import Faker

def generate_user(faker: Faker) -> dict:
    return {
        "first_name": faker.first_name(),
        "last_name": faker.last_name(),
        "email": faker.email(),
        "phone": faker.phone_number(),
        "password": faker.password(length=10, special_chars=True, digits=True),
    }