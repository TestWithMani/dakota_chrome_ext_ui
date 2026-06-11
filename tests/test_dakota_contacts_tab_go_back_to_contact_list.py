import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title('Verify "Go back to contact list" returns to the contacts tab')
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_go_back_to_contact_list(dakota_page):
    """Open a contact, go back, and verify the contacts list is displayed again."""
    DakotaSidebarPage(dakota_page).verify_dakota_contacts_tab_go_back_to_contact_list(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    )
