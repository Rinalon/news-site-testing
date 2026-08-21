import pytest
from playwright.sync_api import expect
from helpers import generate_user
from tests.conftest import USERS

@pytest.fixture(scope="function")
def user_profile(login):
    page = login(**USERS[1])

    page.locator("[role='button'].avatar").click()
    page.get_by_role("link", name="Профиль").click()
    expect(page).to_have_url("https://archiscope.ru/profile", timeout=10000)

    return page

def test_change_user_data(faker, user_profile):
    new_data = generate_user(faker, exclude=("email", "password"))

    user_profile.locator("input[name=\"first_name\"]").fill(new_data["first_name"])
    user_profile.locator("input[name=\"last_name\"]").fill(new_data["last_name"])
    user_profile.locator("input[name=\"phone\"]").fill(new_data["phone"])

    user_profile.get_by_role("button", name="Сохранить").click()

    expect(user_profile.get_by_text("Профиль обновлён")).to_be_visible()
