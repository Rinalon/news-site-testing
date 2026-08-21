import pytest
import re
from helpers import generate_news
from playwright.sync_api import expect
from tests.conftest import USERS
from pages import MainPage, NewsCreatingPage, NewsPage

@pytest.fixture(scope="function")
def news_create(login):
    page = login(**USERS[0])
    page.create_news_btn.click()

    expect(page.page).to_have_url("https://archiscope.ru/news/create", timeout=10000)

    return NewsCreatingPage(page.page)

@pytest.fixture
def news_factory(fake):
    def _create(**kwargs):
        return generate_news(fake, **kwargs)
    return _create


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
        id="void form"
    )
])
def test_invalid_news_create(news_create, news_factory, news_config) -> None:
    news = news_factory(**news_config)

    news_create.title_input.fill(news.get("title") or "")
    news_create.subtitle_input.fill(news.get("subtitle") or "")
    news_create.text_input.fill(news.get("text") or "")
    news_create.tags_input.fill(news.get("tags") or "")

    if "image" in news and news["image"]:
        news_create.img_load.set_input_files(news["image"])

    news_create.submit_button.click()

    assert news_create.page.url == "https://archiscope.ru/news/create"

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
def test_valid_news_create(news_create, news_factory, news_config) -> None:
    news = news_factory(**news_config)

    news_create.title_input.fill(news["title"])
    news_create.subtitle_input.fill(news.get("subtitle") or "")
    news_create.text_input.fill(news["text"])
    news_create.tags_input.fill(news.get("tags") or "")

    if "image" in news and news["image"] is not None:
        news_create.img_load.set_input_files(news["image"])

    news_create.submit_button.click()

    expect(news_create.page).to_have_url("https://archiscope.ru/", timeout=10000)

    page = MainPage(news_create.page)

    news_link = page.get_by_title(news["title"])
    expect(news_link).to_be_visible()
    news_link.click()

    expect(page.page).to_have_url(re.compile(r"/news/\d+"), timeout=10000)
    page = NewsPage(page.page)

    expect(page.get_heading(news["title"], 1)).to_be_visible(timeout=10000)
    expect(page.get_text(news["text"])).to_be_visible()

    if news.get("subtitle") is not None:
        expect(page.get_heading(news["subtitle"], 2)).to_be_visible()

    if news.get("tags") is not None:
        for tag in news["tags"].split(", "):
            expect(page.get_tag(tag)).to_be_visible()

    if news.get("image") is not None:
        expect(page.get_img_by_alt(news["title"])).to_be_visible()