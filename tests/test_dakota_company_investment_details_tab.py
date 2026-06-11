import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify firm has Investment Details tab")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_investment_details_tab(dakota_page):
    """Open a Firm result and verify the Investment Details tab is available."""
    DakotaSidebarPage(dakota_page).verify_dakota_company_investment_details_tab(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM,
    )
