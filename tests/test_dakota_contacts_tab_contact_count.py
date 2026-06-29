import allure

from utils.config import Config


@allure.title("Verify Contacts tab shows number of results displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_count(dakota_sidebar):
    """Open a company and verify the Contacts tab shows the results count label."""
    dakota_sidebar.verify_dakota_contacts_tab_contact_count(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
