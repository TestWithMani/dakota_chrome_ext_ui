import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify contact details include Email")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_detail_email(dakota_page):
    """Open a company, click the first contact, and verify Email is displayed."""
    DakotaSidebarPage(dakota_page).verify_dakota_contacts_tab_contact_detail_email(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    )
