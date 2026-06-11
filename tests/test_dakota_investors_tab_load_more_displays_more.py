import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify Load More Investors displays more investors")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investors_tab_load_more_displays_more(dakota_page):
    """Open a company, load more investors, and verify additional investors appear."""
    DakotaSidebarPage(dakota_page).verify_dakota_investors_tab_load_more_displays_more(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    )
