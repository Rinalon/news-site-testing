import logging
from abc import ABC, abstractmethod

logger = logging.getLogger("pages")

class BasePage(ABC):
    """Абстрактный базовый класс — не зависит от фреймворка"""

    @abstractmethod
    def goto(self, url): pass

    @abstractmethod
    def take_screenshot(self, name: str): pass