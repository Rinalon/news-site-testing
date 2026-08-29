import allure
import pytest
import re
from helpers import generate_news
from playwright.sync_api import expect
from tests.conftest import USERS
from pages.playwright import MainPage, CreateNewsPage, NewsPage

@allure.epic("News")
@allure.feature("Создание новости")
class TestNewsCreation:
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
        assert isinstance(page, CreateNewsPage), "Произошёл переход на главную страницу"

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
    def test_valid_news_create(self, news_factory, news_config) -> None:
        with allure.step("Создать новость"):
            news = news_factory(**news_config)
            self.news_create.fill_form(**news).submit()

        with allure.step("Проверка создания новости"):
            main_page = self.news_create.redirect()
            assert isinstance(main_page, MainPage), "Не произошёл переход на главную страницу"

            news_link = main_page.get_by_title(news["title"])
            expect(news_link).to_be_visible()
            news_link.click()

        with allure.step("Переход на страницу созданной новости"):
            expect(main_page.page).to_have_url(re.compile(r"/news/\d+"), timeout=10000)
            news_page = NewsPage(main_page.page)

        with allure.step("Проверка заголовка"):
            expect(news_page.get_heading(news["title"], 1)).to_be_visible(timeout=10000)
            expect(news_page.get_text(news["text"])).to_be_visible()

        if news.get("subtitle") is not None:
            with allure.step("Проверка подзаголовка"):
                expect(news_page.get_heading(news["subtitle"], 2)).to_be_visible()

        if news.get("tags") is not None:
            with allure.step("Проверка тегов"):
                for tag in news["tags"].split(", "):
                    expect(news_page.get_tag(tag)).to_be_visible()

        if news.get("image") is not None:
            with allure.step("Проверка картинки"):
                expect(news_page.get_img_by_alt(news["title"])).to_be_visible()