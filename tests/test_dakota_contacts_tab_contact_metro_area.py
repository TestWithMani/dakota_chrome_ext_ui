import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify contact details include Metro Area")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_metro_area(dakota_page):
    """Open a company, click the first contact, and verify Metro Area is displayed."""
    DakotaSidebarPage(dakota_page).verify_dakota_contacts_tab_contact_metro_area(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    )
