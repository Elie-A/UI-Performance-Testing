from pages.base_page import BasePage
from utils.browser_manager import BrowserManager

class LoginPage(BasePage):
    def __init__(self, browser_manager: BrowserManager):
        super().__init__(browser_manager)
        self.username_field = "#user-name"
        self.password_field = "#password"
        self.login_button = "#login-button"
        self.page_title = ".title"

    def login(self, username: str, password: str):
        self.enter_text(self.username_field, username)
        self.enter_text(self.password_field, password)
        self.click_element(self.login_button)
    
    def is_on_page(self) -> bool:
        return self.is_element_present(self.page_title)
