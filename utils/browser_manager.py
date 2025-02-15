from Browser import Browser, SupportedBrowsers, ViewportDimensions
from dotenv import load_dotenv
import os

# Global flag to track if environment variables have been loaded
env_loaded = False

def load_env_variables():
    global env_loaded
    if not env_loaded:
        load_dotenv()  # Load environment variables from .env file
        env_loaded = True  # Set flag to prevent reloading

class BrowserManager:
    # Store the singelton instance
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BrowserManager, cls).__new__(cls, *args, **kwargs)
            cls._instance.browser = Browser()
        return cls._instance

    def open_browser(self, url: str = os.getenv("base_url", "https://www.saucedemo.com/"), is_headless_mode: bool = False):
        # Load environment variables only if not loaded already
        load_env_variables()

        # Retrieve browser type from environment variable and map it to SupportedBrowsers
        browser_type = os.getenv("browser_type", "chromium").lower()
        
        # Ensure the browser type maps to SupportedBrowsers
        try:
            browser_enum = getattr(SupportedBrowsers, browser_type)
        except AttributeError:
            # Default to chromium if the browser type is invalid
            browser_enum = SupportedBrowsers.chromium

        # Set headless mode
        headless_mode = os.getenv("headless_mode", "False").lower() == "true" or is_headless_mode

        # Open a new browser window with the specified headless mode
        self.browser.new_browser(browser=browser_enum, headless = headless_mode)

        # Set browser timeout
        self.browser.set_browser_timeout(timeout = os.getenv("browser_timeout", "30s"))

        # width, height = get_screen_resolution()
        # self.browser.new_context(viewport=ViewportDimensions(width=width, height=height))

        self.browser.new_context()
        self.browser.new_page(url)

    def close_browser(self):
        self.browser.close_browser()

    def get_browser(self):
        return self.browser

# Ensure environment variables are loaded only once
load_env_variables()