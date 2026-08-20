import pytest
import re
from playwright.sync_api import Page, expect, sync_playwright, Playwright
from helpers import generate_user

def test_registration(page: Page, faker):
    page.goto("https://archiscope.ru/")

    user = generate_user(faker)

    page.get_by_role("link", name="Регистрация").click()

    # Заполнение формы Регистрации
    page.locator("input[name=\"first_name\"]").fill(user["first_name"])
    page.locator("input[name=\"last_name\"]").fill(user["last_name"])
    page.locator("input[name=\"email\"]").fill(user["email"])
    page.locator("input[name=\"phone\"]").fill(user["phone"])
    page.locator("input[name=\"password\"]").fill(user["password"])

    page.get_by_role("button", name="Зарегистрироваться").click()

    # Заполнение формы Логина
    page.get_by_role("textbox", name="user@example.com").fill(user["email"])
    page.get_by_role("textbox", name="••••••").fill(user["password"])

    page.get_by_role("button", name="Войти").click()
