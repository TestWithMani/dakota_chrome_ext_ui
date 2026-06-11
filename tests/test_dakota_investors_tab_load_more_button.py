import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify Investors tab has Load More Investors button")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investors_tab_load_more_button(dakota_page):
    """Open a company and verify Load More Investors is visible on the Investors tab."""
    DakotaSidebarPage(dakota_page).verify_dakota_investors_tab_load_more_button(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_INVESTORS_TAB_SEARCH_TERM,
    )
