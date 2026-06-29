import allure

from utils.config import Config


@allure.title("Verify clicking a contact displays contact details")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_details(dakota_sidebar):
    """Open a company, click the first contact, and verify details are displayed."""
    dakota_sidebar.verify_dakota_contacts_tab_contact_details(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
