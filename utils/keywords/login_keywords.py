from robot.api.deco import keyword
from utils.browser_manager import BrowserManager
from pages.login_page import LoginPage
from utils.perf_utils.performance_keywords import performance_keyword

browser_manager = BrowserManager()
login_page = LoginPage(browser_manager)

@performance_keyword("user navigates to application")
@keyword("user navigates to application")
def user_navigates_to_application(headless_mode: bool = False):
    browser_manager.open_browser(is_headless_mode = headless_mode)

@performance_keyword("user login in")
@keyword("user logs in")
def user_logs_in(username: str, password: str):
    login_page.login(username, password)

@performance_keyword("user is on products page")
@keyword("user is on products page")
def user_is_on_products_page() -> bool:
    return login_page.is_on_page() == True