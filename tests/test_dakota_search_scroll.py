import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_SIDEBAR_SEARCH_TERM,
    DAKOTA_USERNAME,
)


@allure.title("Verify Dakota sidebar search results scroll to end")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_search_scroll(dakota_page):
    """Search in the Dakota sidebar and verify results can scroll to the end."""
    DakotaSidebarPage(dakota_page).verify_dakota_search_results_scroll(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_SIDEBAR_SEARCH_TERM,
    )
