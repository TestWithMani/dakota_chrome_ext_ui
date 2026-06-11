import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_COMPANY_DETAILS_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify company details open from Dakota search result")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_details(dakota_page):
    """Search, open a result, and verify company details are displayed."""
    DakotaSidebarPage(dakota_page).verify_dakota_company_details(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_COMPANY_DETAILS_SEARCH_TERM,
    )
