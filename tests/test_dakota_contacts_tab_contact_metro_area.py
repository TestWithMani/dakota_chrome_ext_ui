import allure

from utils.config import Config


@allure.title("Verify contact details include Metro Area")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_metro_area(dakota_sidebar):
    """Open a company, click the first contact, and verify Metro Area is displayed."""
    dakota_sidebar.verify_dakota_contacts_tab_contact_metro_area(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
