import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_EXTERNAL_PAGE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify Dakota sidebar auto-search from LinkedIn company page")
@allure.severity(allure.severity_level.CRITICAL)
def test_dakota_linkedin_company_auto_search(dakota_page):
    """Open LinkedIn company page, open sidebar, and verify prefilled search results."""
    DakotaSidebarPage(dakota_page).verify_external_page_auto_search_results(
        DAKOTA_EXTERNAL_PAGE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
    )
