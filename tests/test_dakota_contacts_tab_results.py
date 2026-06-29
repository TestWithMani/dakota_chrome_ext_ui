import allure

from utils.config import Config


@allure.title("Verify Contacts tab displays contacts")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_results(dakota_sidebar):
    """Open a company and verify the Contacts tab shows contacts or empty state."""
    dakota_sidebar.verify_dakota_contacts_tab_results(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
