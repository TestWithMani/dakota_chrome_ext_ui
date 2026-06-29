import allure

from utils.config import Config


@allure.title("test_dakota_contacts_tab_go_back_to_contact_list")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_go_back_to_contact_list(dakota_sidebar):
    """Open a contact, go back, and verify the contacts list is displayed again."""
    dakota_sidebar.verify_dakota_contacts_tab_go_back_to_contact_list(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
