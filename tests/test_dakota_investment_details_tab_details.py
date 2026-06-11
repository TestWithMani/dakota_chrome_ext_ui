import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify Investment Details tab displays details")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investment_details_tab_details(dakota_page):
    """Open a Firm result and verify Investment Details shows data or empty state."""
    DakotaSidebarPage(dakota_page).verify_dakota_investment_details_tab_details(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM,
    )
