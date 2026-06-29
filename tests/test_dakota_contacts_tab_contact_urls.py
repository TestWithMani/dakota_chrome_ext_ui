import allure

from utils.config import Config


@allure.title("Verify all contacts have their URLs displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_urls(dakota_sidebar):
    """Open a company and verify each contact displays a URL."""
    dakota_sidebar.verify_dakota_contacts_tab_contact_urls(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
