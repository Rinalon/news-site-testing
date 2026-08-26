import allure
import pytest
import re
from helpers import generate_news
from playwright.sync_api import expect
from tests.conftest import USERS, BASE_URL
from pages.playwright import MainPage, NewsCreatingPage, NewsPage

@allure.epic("News")
@allure.feature("Создание новости")
class TestNewsCreation:
    """Тесты создания новостей"""

    @pytest.fixture(autouse=True)
    def setup(self, login, request):
        """Фикстура, которая выполняется перед каждым тестом в классе"""
        main_page = login(**USERS[0])
        self.news_create = NewsCreatingPage(main_page.goto_create_news())

    @pytest.fixture
    def news_factory(self, faker) -> dict:
        """Фикстура для создания новостей внутри класса"""

        def _create(**kwargs) -> dict:
            return generate_news(faker, **kwargs)

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
        pytest.param(
            {"exclude": ("title",)},
            id="without_title"
        ),
        pytest.param(
                {"exclude": ("text",)},
                id="without_text",
        ),
        pytest.param(
            {"exclude": ("title", "subtitle", "text", "tags", "image")},
            id="void_form"
        )
    ])
    def test_invalid_news_create(self, news_factory, news_config):
        news = news_factory(**news_config)
        self.news_create.fill_form(**news)

        assert self.news_create.page.url == f"{BASE_URL}/news/create"

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
        pytest.param(
            {},
            id="full_news"
        ),
        pytest.param(
                {"exclude": ("image",)},
                id="without_image",
        ),
        pytest.param(
               {"exclude": ("subtitle",)},
                id="without_subtitle",
        ),
        pytest.param(
                {"exclude": ("tags",)},
                id="without_tags",
        ),
        pytest.param(
                {"exclude": ("image", "subtitle", "tags",)},
                id="min_news",
        ),
    ])
    def test_valid_news_create(self, news_factory, news_config) -> None:
        with allure.step("Создать новость"):
            news = news_factory(**news_config)
            page = self.news_create.fill_form(**news)

        with allure.step("Проверка создания новости"):
            expect(page).to_have_url(BASE_URL, timeout=10000)
            main_page = MainPage(self.news_create.page)

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