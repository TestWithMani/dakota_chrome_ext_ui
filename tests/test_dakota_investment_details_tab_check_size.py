import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify Investment Details tab displays Check Size")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investment_details_tab_check_size(dakota_page):
    """Open a Firm result and verify Investment Details displays Check Size."""
    DakotaSidebarPage(dakota_page).verify_dakota_investment_details_tab_check_size(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM,
    )
