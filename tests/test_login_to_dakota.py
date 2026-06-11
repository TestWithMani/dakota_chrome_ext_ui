import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Login to Dakota - open extension from toolbar")
@allure.severity(allure.severity_level.NORMAL)
def test_login_to_dakota(dakota_page):
    """Open Dakota Marketplace, open the extension from the toolbar, and log in."""
    DakotaSidebarPage(dakota_page).login_to_dakota_marketplace(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
    )
