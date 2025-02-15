from robot.api.deco import keyword
from utils.perf_utils.performance_keywords import performance_keyword
from pages import products_page
from utils.browser_manager import BrowserManager
from pages.products_page import ProductsPage

browser_manager = BrowserManager()
products_page = ProductsPage(browser_manager)

@performance_keyword("Sort Products")
@keyword("user sorts products")
def user_sorts_products(attribute: str, option_text: str):
    return products_page.sort_products(attribute, option_text)

@performance_keyword("Validate Products Sorting")
@keyword("products are sorted")
def products_are_sorted(option_text: str) -> bool:
    return  products_page.validate_product_sort(option_text) == True