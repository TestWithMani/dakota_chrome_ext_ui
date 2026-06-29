import allure

from utils.config import Config


@allure.title("Verify Contacts tab Load more matches General tab contact count")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_load_more_button(dakota_sidebar):
    """Open a company and verify Load more visibility matches the contact count."""
    dakota_sidebar.verify_dakota_contacts_tab_load_more_button(
        Config.DAKOTA_CONTACTS_LOAD_MORE_BUTTON_SEARCH_TERM
    )
