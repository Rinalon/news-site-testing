import allure
import pytest
from selenium.webdriver.support import expected_conditions as EC
from helpers import generate_news
from tests.conftest import USERS, BASE_URL
from pages.selenium import MainPage, CreateNewsPage, NewsPage


class TestNewsCreating:
    """Тесты создания новостей"""

    @pytest.fixture(autouse=True)
    def setup(self, login):
        """Фикстура для перехода на страницу создания новости"""
        main_page = login(**USERS[0])
        self.news_create = main_page.goto_create_news()

    @pytest.fixture
    def news_factory(self, fake) -> dict:
        """Фикстура для создания новостей внутри класса"""

        def _create(**kwargs) -> dict:
            return generate_news(fake, **kwargs)

        return _create

    @allure.story("Негативные сценарии")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    1 Логин под тестовым пользователем
    2 Переход на страницу создания новости
    3 Генерация новости
    4 Заполнение формы
    5 Нажать на кнопку создания
    5 Проверка, что мы остались на странице формы 
    """)
    @pytest.mark.parametrize("news_config", [
        pytest.param({"exclude": ("title",)}, id="without_title"),
        pytest.param({"exclude": ("text",)}, id="without_text", ),
        pytest.param(
            {"exclude": ("title", "subtitle", "text", "tags", "image")}, id="void_form"
        )
    ])
    def test_invalid_news_create(self, news_factory, news_config):
        news = news_factory(**news_config)

        self.news_create.fill_form(**news).submit()
        page = self.news_create.redirect()

        assert isinstance(page, CreateNewsPage)

    @allure.story("Позитивный сценарии")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
        1 Логин под тестовым пользователем
        2 Переход на страницу создания новости
        3 Генерация новости
        4 Заполнение формы
        5 Нажать на кнопку создания
        5 Проверка, что мы оказались на главной странице
        6 Проверка существования новости с таким заголовком на главной странице
        7 Переход на страницу новости
        8 Проверка на соответствие заполнения исходным данным и фактическим данным
    """)
    @pytest.mark.parametrize("news_config", [
        pytest.param({}, id="full_news"),
        pytest.param({"exclude": ("image",)}, id="without_image"),
        pytest.param({"exclude": ("subtitle",)}, id="without_subtitle"),
        pytest.param({"exclude": ("tags",)}, id="without_tags"),
        pytest.param({"exclude": ("image", "subtitle", "tags")}, id="min_news"),
    ])
    def test_valid_news_create(self, news_factory, news_config):
        with allure.step("Создать новость"):
            news = news_factory(**news_config)
            self.news_create.fill_form(**news).submit()

        with allure.step("Проверка создания новости"):
            main_page = self.news_create.redirect()
            assert isinstance(main_page, MainPage)

            news_locator = main_page.get_by_title(news["title"])

            assert main_page.is_element_visible(news_locator), "Новость не найдена на главной странице"
            main_page.click(news_locator)

        with allure.step("Переход на страницу созданной новости"):
            main_page.wait_for_url_contains("/news/")
            news_page = NewsPage(main_page.driver)

        with allure.step("Проверка заголовка"):
            heading_locator = news_page.get_heading(news["title"], 1)
            assert news_page.is_element_visible(heading_locator), "Заголовок не отображается"

            text_locator = news_page.get_text(news["text"])
            assert news_page.is_element_visible(text_locator), "Текст новости не отображается"

        if news.get("subtitle") is not None:
            with allure.step("Проверка подзаголовка"):
                subtitle_locator = news_page.get_heading(news["subtitle"], 2)
                assert news_page.is_element_visible(subtitle_locator), "Подзаголовок не отображается"

        if news.get("tags") is not None:
            with allure.step("Проверка тегов"):
                for tag in news["tags"].split(", "):
                    tag_locator = news_page.get_tag(tag)
                    assert news_page.is_element_visible(tag_locator), f"Тег '{tag}' не отображается"

        if news.get("image") is not None:
            with allure.step("Проверка картинки"):
                img_locator = news_page.get_img_by_alt(news["title"])
                assert news_page.is_element_visible(img_locator), "Изображение не отображается"