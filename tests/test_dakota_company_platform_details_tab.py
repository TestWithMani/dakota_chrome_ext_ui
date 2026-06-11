import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_PLATFORM_DETAILS_TAB_SEARCH_TERM,
    DAKOTA_USERNAME,
)


@allure.title("Verify allocator has Platform Details tab")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_platform_details_tab(dakota_page):
    """Open an Allocator result and verify the Platform Details tab is available."""
    DakotaSidebarPage(dakota_page).verify_dakota_company_platform_details_tab(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_PLATFORM_DETAILS_TAB_SEARCH_TERM,
    )
