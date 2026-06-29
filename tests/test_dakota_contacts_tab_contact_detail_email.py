import allure

from utils.config import Config


@allure.title("Verify contact details include Email")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_detail_email(dakota_sidebar):
    """Open a company, click the first contact, and verify Email is displayed."""
    dakota_sidebar.verify_dakota_contacts_tab_contact_detail_email(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
