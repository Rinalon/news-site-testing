import allure
import pytest
from playwright.sync_api import expect
from pages.playwright import MainPage
from tests.conftest import BASE_URL

@allure.epic("News")
@allure.feature("Пагинация")
@allure.story("Навигация по страницам")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
1 Переход на главную страницу сайта
2 Ждём загрузки новостей
3 Проверяем цифры на нижней панели
5 Проверяем работу кнопки '»' и '«'
6 Проверяем их отключение на последней и первой странице соответственно 
""")
def test_pagination(page):
    with allure.step("Открыть главную страницу"):
        main_page = MainPage(page).goto(BASE_URL)

    with allure.step("Дождаться загрузки новостей на первой странице"):
        first_news_title = main_page.news_titles.first
        expect(first_news_title).to_be_visible()
        titles_page1 = main_page.news_titles.all_text_contents()
        allure.attach(
            str(titles_page1[:3]),
            name="Первые 3 заголовка на странице 1",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Перейти на вторую страницу"):
        main_page.get_page(2).click(timeout=10000)
        expect(main_page.active_page).to_have_text("2")
        titles_page2 = main_page.news_titles.all_text_contents()
        allure.attach(
            str(titles_page2[:3]),
            name="Первые 3 заголовка на странице 2",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Проверить, что заголовки новостей изменились"):
        assert titles_page1 != titles_page2, "Заголовки новостей не изменились при переходе на страницу 2"

    with allure.step("Перейти на третью страницу через кнопку '»'"):
        main_page.next_button.click(timeout=10000)
        expect(main_page.active_page).to_have_text("3")

    with allure.step("Вернуться на вторую страницу через кнопку '«'"):
        main_page.prev_button.click()
        expect(main_page.active_page).to_have_text("2")

    with allure.step("Перейти на последнюю страницу"):
        last_page_text = main_page.page_buttons.last.text_content()
        main_page.page_buttons.last.click()
        expect(main_page.active_page).to_have_text(last_page_text)
        allure.attach(
            f"Номер последней страницы: {last_page_text}",
            name="Информация о странице",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Проверить, что кнопка '»' отключена на последней странице"):
        expect(main_page.next_button).to_be_disabled()

    with allure.step("Перейти на первую страницу"):
        first_page_text = main_page.page_buttons.first.text_content()
        assert first_page_text == "1", "Первая страница в нижнем меню названа неправильно"
        main_page.page_buttons.first.click()
        expect(main_page.active_page).to_have_text("1")

    with allure.step("Проверить, что кнопка '«' отключена на первой странице"):
        expect(main_page.prev_button).to_be_disabled()
