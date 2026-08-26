import allure
from pathlib import Path
from pages.base import logger, BasePage as AbstractPage

class BasePage(AbstractPage):
    def __init__(self, page):
        self.page = page

    def goto(self, url):
        logger.info(f"Переход на страницу {url}")
        with allure.step(f"Переход на страницу {url}"):
            self.page.goto(url)
            self.page.wait_for_load_state("networkidle")
        logger.info(f"Страница загружена {url}")
        return self

    def take_screenshot(self, name: str):
        screenshot_path = f"artifacts/screenshots/{name}.png"
        Path("artifacts/screenshots/").mkdir(parents=True, exist_ok=True)
        self.page.screenshot(path=screenshot_path, full_page=True)

        logger.info(f"Сделан скриншот {screenshot_path}")
        allure.attach.file(screenshot_path, name = name, attachment_type="image/png")
