import allure

from utils.config import Config


@allure.title("Verify Contacts tab search bar returns search results")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_search_results(dakota_sidebar):
    """Open a company and verify the Contacts search bar returns results."""
    dakota_sidebar.verify_dakota_contacts_tab_search_results(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM,
        Config.DAKOTA_CONTACTS_TAB_CONTACT_SEARCH_TERM,
    )
