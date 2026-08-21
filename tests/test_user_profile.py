import pytest
from playwright.sync_api import expect
from helpers import generate_user
from tests.conftest import USERS
from pages import UserProfilePage

@pytest.fixture(scope="function")
def user_profile(login):
    page = login(**USERS[1])

    page.avatar.click()
    page.profile_button.click()
    expect(page.page).to_have_url("https://archiscope.ru/profile", timeout=10000)

    return UserProfilePage(page.page)

def test_change_user_data(faker, user_profile):
    new_data = generate_user(faker, exclude=("email", "password"))

    user_profile.first_name_input.fill(new_data["first_name"])
    user_profile.last_name_input.fill(new_data["last_name"])
    user_profile.phone_input.fill(new_data["phone"])

    user_profile.save_button.click()

    expect(user_profile.access_message).to_be_visible()
