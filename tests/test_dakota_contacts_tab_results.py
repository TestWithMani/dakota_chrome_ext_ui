import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify Contacts tab displays contacts")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_results(dakota_page):
    """Open a company and verify the Contacts tab shows contacts or empty state."""
    DakotaSidebarPage(dakota_page).verify_dakota_contacts_tab_results(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    )
