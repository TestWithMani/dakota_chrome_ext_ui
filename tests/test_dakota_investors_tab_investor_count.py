import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify Investors tab shows number of investors displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investors_tab_investor_count(dakota_page):
    """Open a company and verify the Investors tab shows the investor count label."""
    DakotaSidebarPage(dakota_page).verify_dakota_investors_tab_investor_count(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    )
