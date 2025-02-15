from utils.browser_manager import BrowserManager
from Browser import SelectAttribute

class BasePage:
    def __init__(self, browser_manager: BrowserManager):
        self.browser = browser_manager.get_browser()

    def open_url(self, url: str):
        self.browser.new_page(url)

    def click_element(self, locator: str):
        self.browser.click(locator)  

    def enter_text(self, locator: str, text: str):
        self.browser.type_text(locator, text)  

    def is_element_present(self, locator: str) -> bool:
        try:
            self.browser.get_element(locator)
            return True
        except Exception:
            return False
    
    def select_item_from_dropdown(self, dropdown_locator: str, attribute: str, option_text: str):
        if attribute not in ["value", "label", "text", "index"]:
            raise ValueError("Invalid attribute for dropdown selection. Use SelectAttribute.value, SelectAttribute.label, SelectAttribute.text or SelectAttribute.index")
        if attribute == "value":
            self.browser.select_options_by(dropdown_locator, SelectAttribute.value, option_text)
        elif attribute == "label":
            self.browser.select_options_by(dropdown_locator, SelectAttribute.label, option_text)
        elif attribute == "text":
            self.browser.select_options_by(dropdown_locator, SelectAttribute.text, option_text)
        elif attribute == "index":
            self.browser.select_options_by(dropdown_locator, SelectAttribute.index, option_text)

    def get_elements_text(self, locator: str) -> list:
        # Use the Browser library to get elements matching the selector
        elements = self.browser.get_elements(locator)
        # Extract the text from each element and return as a list
        return [self.browser.get_text(element) for element in elements]
