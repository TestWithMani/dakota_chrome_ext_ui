import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_COMPANY_DETAILS_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify Dakota company General tab Account Overview")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_account_overview(dakota_page):
    """Open a company and verify Account Overview is displayed on the General tab."""
    DakotaSidebarPage(dakota_page).verify_dakota_company_account_overview(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_COMPANY_DETAILS_SEARCH_TERM,
    )
