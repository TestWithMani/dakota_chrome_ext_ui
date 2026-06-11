import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_PLATFORM_DETAILS_TAB_SEARCH_TERM,
    DAKOTA_USERNAME,
)


@allure.title("Verify Platform Details tab displays Platform Description")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_platform_details_tab_platform_description(dakota_page):
    """Open a company and verify Platform Details displays Platform Description."""
    DakotaSidebarPage(
        dakota_page
    ).verify_dakota_platform_details_tab_platform_description(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_PLATFORM_DETAILS_TAB_SEARCH_TERM,
    )
