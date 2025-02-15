# Updated ProductsPage in `products_page.py`
from pages.base_page import BasePage
from utils.browser_manager import BrowserManager
from utils.miscUtils import is_list_of_strings_sorted, is_list_of_numbers_sorted

class ProductsPage(BasePage):
    def __init__(self, browser_manager: BrowserManager):
        super().__init__(browser_manager)
        self.title = ".title"
        self.dropdown = ".product_sort_container"
        self.totalInCart = ".shopping_cart_badge"
        self.shoppingCart = ".shopping_cart_link"
        self.inventoryItemsList = ".inventory_item_name"
        self.itemPricesList = ".inventory_item_price"

    def sort_products(self, attribute: str, option_text: str):
        self.select_item_from_dropdown(self.dropdown, attribute, option_text)
    
    def validate_product_sort(self, option_text: str) -> bool:
        if option_text == "Name (A to Z)":
            items_list = self.get_elements_text(self.inventoryItemsList)
            return is_list_of_strings_sorted(items_list, "ASC")
        elif option_text == "Name (Z to A)":
            items_list = self.get_elements_text(self.inventoryItemsList)
            return is_list_of_strings_sorted(items_list, "DESC")
        elif option_text == "Price (low to high)":
            items_price_list = self.get_elements_text(self.itemPricesList)
            return is_list_of_numbers_sorted(items_price_list, "ASC")
        elif option_text == "Price (high to low)":
            items_price_list = self.get_elements_text(self.itemPricesList)
            return is_list_of_numbers_sorted(items_price_list, "DESC")