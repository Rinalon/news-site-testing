import pytest
from playwright.sync_api import Page, expect
from pages import MainPage

def test_pagination(page: Page):
    page.goto("https://archiscope.ru/")
    main_page = MainPage(page)
    
    # Ждём загрузки карточек новостей
    first_news_title = main_page.news_titles.first
    expect(first_news_title).to_be_visible()

    titles_page1 = main_page.news_titles.all_text_contents()

    # Переходим на 2ю страницу
    main_page.get_page(2).click()
    expect(main_page.active_page).to_have_text("2")

    titles_page2 = main_page.news_titles.all_text_contents()

    assert titles_page1 != titles_page2, "Заголовки новостей не изменились при переходе на страницу 2"

    # Проверяем кнопку »
    main_page.next_button.click()
    expect(main_page.active_page).to_have_text("3")

    # Проверяем кнопку «
    main_page.prev_button.click()
    expect(main_page.active_page).to_have_text("2")

    # Проверяем переход на последнюю страницу
    last_page_text = main_page.page_buttons.last.text_content()
    main_page.page_buttons.last.click()

    expect(main_page.active_page).to_have_text(last_page_text)
    expect(main_page.next_button).to_be_disabled()

    # Проверяем переход на первую страницу
    first_page_text = main_page.page_buttons.first.text_content()
    assert first_page_text == "1", "первая страница в нижнем меню названа неправильно"

    main_page.page_buttons.first.click()
    expect(main_page.active_page).to_have_text("1")

    expect(main_page.prev_button).to_be_disabled()
