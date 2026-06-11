import allure

from pages.chrome_web_store_page import ChromeWebStorePage
from pages.google_home_page import GoogleHomePage
from utils.config import Config


@allure.title("Search Dakota extension from Chrome Web Store")
@allure.severity(allure.severity_level.CRITICAL)
def test_dakota_extension_installation(page):
    web_store_tab = GoogleHomePage(page).open_chrome_web_store_tab(
        Config.BASE_URL,
        Config.WEB_STORE_URL,
    )
    ChromeWebStorePage(web_store_tab).install_dakota_marketplace_extension(
        Config.SEARCH_TERM
    )
