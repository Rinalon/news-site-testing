import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from pages.selenium.main_page import MainPage
from tests.conftest import BASE_URL


@allure.epic("News")
@allure.feature("Пагинация")
@allure.story("Навигация по страницам")
@allure.severity(allure.severity_level.CRITICAL)
@allure.description("""
1. Переход на главную страницу сайта
2. Ждём загрузки новостей
3. Проверяем цифры на нижней панели
4. Проверяем работу кнопки '»' и '«'
5. Проверяем их отключение на последней и первой странице соответственно
""")
def test_pagination(context):
    with allure.step("Открыть главную страницу"):
        main_page = MainPage(context).goto(BASE_URL)

    with allure.step("Дождаться загрузки новостей на первой странице"):
        assert main_page.is_element_visible(main_page.news_titles), "Не отображаются новости"

        titles_page1 = main_page.get_texts(main_page.news_titles)
        allure.attach(
            str(titles_page1[:3]),
            name="Первые 3 заголовка на странице 1",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Перейти на вторую страницу"):
        first_title_before = main_page.get_texts(main_page.news_titles)[0]

        page_2_locator = main_page.get_page_button(2)
        main_page.click(page_2_locator)


        main_page.is_text_present_in_element(main_page.active_page, "2")

        with allure.step("Ждём, пока текст 1й новости изменится"):
            WebDriverWait(main_page.driver, 10).until(
                lambda d: main_page.get_texts(main_page.news_titles)[0] != first_title_before
            )

        titles_page2 = main_page.get_texts(main_page.news_titles)
        allure.attach(
            str(titles_page2[:3]),
            name="Первые 3 заголовка на странице 2",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Проверить, что заголовки новостей изменились"):
        assert titles_page1 != titles_page2, "Заголовки новостей не изменились при переходе на страницу 2"

    with allure.step("Перейти на третью страницу через кнопку '»'"):
        main_page.next_click()
        main_page.is_text_present_in_element(main_page.active_page, "3")
        main_page.is_element_visible(main_page.news_titles)

    with allure.step("Вернуться на вторую страницу через кнопку '«'"):
        main_page.prev_click()
        main_page.is_text_present_in_element(main_page.active_page, "2")
        main_page.is_element_visible(main_page.news_titles)

    with allure.step("Перейти на последнюю страницу"):
        page_buttons = main_page.find_all(main_page.page_buttons)
        last_button = page_buttons[-1]
        last_page_text = last_button.text
        last_button.click()
        main_page.is_text_present_in_element(main_page.active_page, last_page_text)
        main_page.is_element_visible(main_page.news_titles)
        allure.attach(
            f"Номер последней страницы: {last_page_text}",
            name="Информация о странице",
            attachment_type=allure.attachment_type.TEXT
        )

    with allure.step("Проверить, что кнопка '»' отключена на последней странице"):
        assert main_page.is_element_disabled(main_page.next_button), "Кнопка '»' не отключена на последней странице"

    with allure.step("Перейти на первую страницу"):
        first_button = main_page.find_all(main_page.page_buttons)[0]
        first_page_text = first_button.text
        assert first_page_text == "1", "Первая страница в нижнем меню названа неправильно"
        first_button.click()
        main_page.is_text_present_in_element(main_page.active_page, "1")
        main_page.is_element_visible(main_page.news_titles)

    with allure.step("Проверить, что кнопка '«' отключена на первой странице"):
        assert main_page.is_element_disabled(main_page.prev_button), "Кнопка '«' не отключена на первой странице"