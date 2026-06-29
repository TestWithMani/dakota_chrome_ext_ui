import allure

from utils.config import Config


@allure.title("Verify all contacts have their email addresses displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_emails(dakota_sidebar):
    """Open a company and verify each contact displays an email address."""
    dakota_sidebar.verify_dakota_contacts_tab_contact_emails(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
