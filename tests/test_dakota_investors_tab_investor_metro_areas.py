import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify all investors have their states/cities displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investors_tab_investor_metro_areas(dakota_page):
    """Open a company, scroll the Investors tab, and verify each investor has a state/city."""
    DakotaSidebarPage(dakota_page).verify_dakota_investors_tab_investor_metro_areas(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    )
