import allure
import pytest

from helpers import generate_user
from tests.conftest import USERS

@pytest.fixture(scope="function")
def profile_page(login):
    """
        Фикстура для перехода на страницу пользователя
        Returns:
            UserProfilePage: страница пользователя
    """
    main_page = login(**USERS[1])
    return main_page.goto_profile()

@allure.epic("User Profile")
@allure.feature("Изменение данных пользователя")
@allure.story("Позитивный тест")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("""
1 Логин под тестовым пользователем
2 Переход на профиль
3 Генерируем новые данные пользователя
4 Сохранениям их
5 Проверяем наличие сообщение о успехе

Игнорируем email и password, чтобы не менять тестового пользователя
""")
def test_change_user_data(fake, profile_page):
    new_data = generate_user(fake, exclude=("email", "password"))

    profile_page.fill_first_name(new_data["first_name"])
    profile_page.fill_last_name(new_data["last_name"])
    profile_page.fill_phone(new_data["phone"])

    profile_page.click_save_button()

