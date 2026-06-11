import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_COMPANY_DETAILS_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify Contacts tab count matches General tab stat")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_contacts_count(dakota_page):
    """Open a company and verify Contacts tab items match General tab Contacts count."""
    DakotaSidebarPage(dakota_page).verify_dakota_contacts_count_matches_general_tab(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_COMPANY_DETAILS_SEARCH_TERM,
    )
