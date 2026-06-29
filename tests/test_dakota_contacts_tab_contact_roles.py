import allure

from utils.config import Config


@allure.title("Verify all contacts have their roles displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_roles(dakota_sidebar):
    """Open a company and verify each contact displays a role."""
    dakota_sidebar.verify_dakota_contacts_tab_contact_roles(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
