import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify clicking a contact displays contact details")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_details(dakota_page):
    """Open a company, click the first contact, and verify details are displayed."""
    DakotaSidebarPage(dakota_page).verify_dakota_contacts_tab_contact_details(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    )
