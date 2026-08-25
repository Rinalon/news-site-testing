import os
import random
import requests
from pathlib import Path
from faker import Faker
from PIL import Image, ImageDraw

def generate_image(
        width: int | None = 800,
        height: int | None = 600,
        folder: str | None = None,
) -> str:
    if folder is None:
        this_folder = Path(__file__)
        folder = os.path.join(this_folder.parent.parent, 'temp')


    color = (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )

    img = Image.new("RGB", (width, height), color=color)
    draw = ImageDraw.Draw(img)

    draw.rectangle([0, 0, width - 1, height - 1], outline="black", width=2)

    save_path = os.path.join(folder, f"gen_{random.randint(0, 1000)}.png")
    img.save(save_path, "PNG")
    return save_path

def download_image(
        faker: Faker,
        width: int | None = 800,
        height: int | None = 600,
        folder: str | None = None,
    ) -> str:

    if folder is None:
        this_folder = Path(__file__)
        folder = os.path.join(this_folder.parent.parent, 'temp')

    url = faker.image_url(width=width, height=height)

    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to download image: {response.status_code}")

    filename = f"{faker.uuid4()}.jpg"
    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as f:
        f.write(response.content)

    return os.path.abspath(filepath)

def generate_news(
        faker: Faker,
        words_title: int | None = 5,
        words_subtitle: int | None = 5,
        sentences_count: int | None = 3,
        tags_count: int | None = 5,
        img_width: int = 800,
        img_height: int = 600,
        exclude: tuple[str] | None = None
) -> dict:

    news = {
        "title": faker.sentence(nb_words=words_title),
        "subtitle": faker.sentence(nb_words=words_subtitle),
        "text": faker.paragraph(nb_sentences=sentences_count),
        "tags": ", ".join(faker.words(nb=tags_count)),
    }

    try:
        img_path = download_image(faker, width=img_width, height=img_height)
    except:
        img_path = generate_image(width=img_width, height=img_height)

    news["image"] = img_path

    if exclude:
        for word in exclude:
            news.pop(word, None)

    return news