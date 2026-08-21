
class UserProfilePage():
    def __init__(self, page):
        self.page = page

        self.first_name_input = page.locator("input[name=\"first_name\"]")
        self.last_name_input = page.locator("input[name=\"last_name\"]")
        self.phone_input = page.locator("input[name=\"phone\"]")
        self.save_button = page.get_by_role("button", name="Сохранить")

        self.access_message = page.get_by_text("Профиль обновлён")