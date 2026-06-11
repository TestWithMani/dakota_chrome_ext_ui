import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify private company has Investors tab")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_investors_tab(dakota_page):
    """Open a private company and verify the Investors tab is available."""
    DakotaSidebarPage(dakota_page).verify_dakota_company_investors_tab(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    )
