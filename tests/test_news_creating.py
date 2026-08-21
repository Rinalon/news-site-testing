import pytest
import re
from helpers import generate_news
from playwright.sync_api import expect

@pytest.fixture(scope="function")
def news_create(login):
    login.locator("a[href='/news/create']").click()
    return login

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

    news_create.locator("input[name='title']").fill(news.get("title") or "")
    news_create.locator("input[name='subtitle']").fill(news.get("subtitle") or "")
    news_create.locator("textarea[name='text']").fill(news.get("text") or "")
    news_create.locator("input[name='tags']").fill(news.get("tags") or "")

    if "image" in news and news["image"]:
        news_create.locator("input[type='file']").set_input_files(news["image"])

    news_create.locator("button[type=\"submit\"]").click()

    assert news_create.url == "https://archiscope.ru/news/create"

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

    news_create.locator("input[name=\"title\"]").fill(news["title"])
    news_create.locator("input[name=\"subtitle\"]").fill(news.get("subtitle") or "")
    news_create.locator("textarea[name=\"text\"]").fill(news["text"])
    news_create.locator("input[name=\"tags\"]").fill(news.get("tags") or "")

    if "image" in news and news["image"] is not None:
        news_create.locator("input[type='file']").set_input_files(news["image"])

    news_create.locator("button[type=\"submit\"]").click()

    expect(news_create).to_have_url("https://archiscope.ru/", timeout=10000)
    expect(news_create.get_by_text(news["title"])).to_be_visible()

    news_create.get_by_text(news["title"]).click()
    expect(news_create).to_have_url(re.compile(r"/news/\d+"), timeout=10000)

    expect(news_create.get_by_role("heading", name=news["title"], level=1)).to_be_visible(timeout=10000)
    expect(news_create.get_by_text(news["text"])).to_be_visible()

    if news.get("subtitle") is not None:
        expect(news_create.get_by_role("heading", name=news["subtitle"], level=2)).to_be_visible()

    if news.get("tags") is not None:

        for tag in news["tags"].split(", "):
            expect(news_create.locator(f"span:has-text(\"{tag}\")")).to_be_visible()

    if news.get("image") is not None:
        expect(news_create.locator(f"img[alt=\"{news["title"]}\"]")).to_be_visible()