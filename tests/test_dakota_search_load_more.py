import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_SIDEBAR_SEARCH_TERM,
    DAKOTA_USERNAME,
)


@allure.title("Verify Dakota sidebar Load more displays additional results")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_search_load_more(dakota_page):
    """Search, scroll to end, click Load more, and verify more results appear."""
    DakotaSidebarPage(dakota_page).verify_dakota_search_results_load_more(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_SIDEBAR_SEARCH_TERM,
    )
