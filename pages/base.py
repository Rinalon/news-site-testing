from abc import ABC, abstractmethod

class BasePage(ABC):
    """Абстрактный базовый класс — не зависит от фреймворка"""

    BASE_URL = "https://archiscope.ru/"

    @abstractmethod
    def goto(self, url): pass