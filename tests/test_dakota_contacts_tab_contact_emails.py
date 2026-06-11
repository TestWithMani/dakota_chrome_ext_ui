import allure

from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.config import (
    DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    DAKOTA_MARKETPLACE_URL,
    DAKOTA_PASSWORD,
    DAKOTA_USERNAME,
)


@allure.title("Verify all contacts have their email addresses displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_emails(dakota_page):
    """Open a company and verify each contact displays an email address."""
    DakotaSidebarPage(dakota_page).verify_dakota_contacts_tab_contact_emails(
        DAKOTA_MARKETPLACE_URL,
        DAKOTA_USERNAME,
        DAKOTA_PASSWORD,
        DAKOTA_CONTACTS_TAB_SEARCH_TERM,
    )
