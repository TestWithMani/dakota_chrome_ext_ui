import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_SIDEBAR_SEARCH_TERM,
    DAKOTA_USERNAME,
)


@allure.title("Verify Dakota sidebar search results and API response")
@allure.severity(allure.severity_level.CRITICAL)
def test_dakota_search_results(dakota_page):
    """Search in the Dakota extension sidebar and verify results plus API 200."""
    DakotaSidebarPage(dakota_page).verify_dakota_search_results(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_SIDEBAR_SEARCH_TERM,
    )
