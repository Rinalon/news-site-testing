import pytest
from playwright.sync_api import Page, expect


def test_pagination(page: Page):
    page.goto("https://archiscope.ru/")

    # Ждём загрузки карточек новостей
    first_news_title = page.locator(".card-title a").first
    expect(first_news_title).to_be_visible()

    titles_page1 = page.locator(".card-title a").all_text_contents()

    # Переходим на 2ю страницу
    page.locator(".join .btn:has-text('2')").click()

    active_page = page.locator(".join .btn-primary")
    expect(active_page).to_have_text("2")


    titles_page2 = page.locator(".card-title a").all_text_contents()

    assert titles_page1 != titles_page2, "Заголовки новостей не изменились при переходе на страницу 2"

    # Проверяем кнопку »
    next_btn = page.locator(".join .btn:has-text('»')")
    next_btn.click()

    active_page = page.locator(".join .btn-primary")
    expect(active_page).to_have_text("3")

    # Проверяем кнопку «
    prev_btn = page.locator(".join .btn:has-text('«')")
    prev_btn.click()
    active_page = page.locator(".join .btn-primary")
    expect(active_page).to_have_text("2")

    # Проверяем переход на последнюю страницу
    all_page_buttons = page.locator(".join .btn:not(.btn-disabled):not(:has-text('«')):not(:has-text('»'))")
    last_page_text = all_page_buttons.last.text_content()
    all_page_buttons.last.click()
    active_page = page.locator(".join .btn-primary")
    expect(active_page).to_have_text(last_page_text)

    next_btn = page.locator(".join .btn:has-text('»')")
    expect(next_btn).to_be_disabled()

    # Проверяем переход на первую страницу
    first_page_text = all_page_buttons.first.text_content()
    assert first_page_text == "1", "первая страница в нижнем меню названа неправильно"
    all_page_buttons.first.click()
    active_page = page.locator(".join .btn-primary")
    expect(active_page).to_have_text("1")

    next_btn = page.locator(".join .btn:has-text('«')")
    expect(next_btn).to_be_disabled()
