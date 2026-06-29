import allure

from utils.config import Config


@allure.title("Verify contact details include Contact Type")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_type(dakota_sidebar):
    """Open a company, click the first contact, and verify Contact Type is displayed."""
    dakota_sidebar.verify_dakota_contacts_tab_contact_type(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
