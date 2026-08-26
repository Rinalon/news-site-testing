import allure
from selenium.webdriver.common.by import By
from pages.selenium.base import BasePage

class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.create_news_btn = (By.CSS_SELECTOR, "a[href='/news/create']")
        self.login_button = (By.CSS_SELECTOR, "a[href='/login']")
        self.register_button = (By.CSS_SELECTOR, "a[href='/register']")

        self.next_button = (By.XPATH, "//button[text()='»']")
        self.prev_button = (By.XPATH, "//button[text()='«']")

        self.avatar = (By.CSS_SELECTOR, "[role='button'].avatar")
        self.profile_button = (By.CSS_SELECTOR, "a[href='/profile']")

        self.news_titles = (By.CSS_SELECTOR, ".card-title a")
        self.active_page = (By.CSS_SELECTOR, ".join .btn-primary")


        self.page_buttons = (By.XPATH,
                             ".//div[contains(@class, 'join')]//button[not(contains(@class, 'btn-disabled')) and not(text()='«') and not(text()='»')]")

    @allure.step("Получение кнопки страницы по номеру")
    def get_page_button(self, number: int):
        return (By.XPATH, f".//div[contains(@class, 'join')]//button[text()='{number}']")

    @allure.step("Получение номера активной страницы")
    def get_active_page_number(self) -> str:
        element = self.find(self.active_page)
        return element.text

    @allure.step("Поиск новости по заголовку")
    def get_by_title(self, title):
        return (By.XPATH, f"//*[text()='{title}']")

    @allure.step("Переход к странице логина")
    def goto_login(self):
        self.click(self.login_button)
        self.wait_for_url_contains("/login")
        from pages.selenium.login import LoginPage
        return LoginPage(self.driver)

    @allure.step("Переход к странице регистрации")
    def goto_register(self):
        self.click(self.register_button)
        self.wait_for_url_contains("/register")
        from pages.selenium.register import RegisterPage
        return RegisterPage(self.driver)

    @allure.step("Переход к странице профиля")
    def goto_profile(self):
        self.click(self.avatar)
        self.click(self.profile_button)
        self.wait_for_url_contains("/profile")
        from pages.selenium.profile import ProfilePage
        return ProfilePage(self.driver)

    @allure.step("Переход к странице создания новости")
    def goto_create_news(self):
        self.click(self.create_news_btn)
        self.wait_for_url_contains("/news/create")
        from pages.selenium.create_news import CreateNewsPage
        return CreateNewsPage(self.driver)