import pytest
from helpers import generate_user
from tests.conftest import USERS
from pages import UserProfilePage

@pytest.fixture(scope="function")
def user_profile(login):
    page = login(**USERS[1])
    return UserProfilePage(page.goto_profile())

def test_change_user_data(faker, user_profile):
    new_data = generate_user(faker, exclude=("email", "password"))

    user_profile.fill_first_name(new_data["first_name"])
    user_profile.fill_last_name(new_data["last_name"])
    user_profile.fill_phone(new_data["phone"])

    user_profile.click_save_button()
