from abc import ABC, abstractmethod

class BasePage(ABC):
    """Абстрактный базовый класс — не зависит от фреймворка"""

    @abstractmethod
    def goto(self, url):
        pass