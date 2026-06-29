import allure

from utils.config import Config


@allure.title("Verify contact details include LinkedIn URL")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_contact_detail_linkedin_url(dakota_sidebar):
    """Open a company, click the first contact, and verify LinkedIn URL is displayed."""
    dakota_sidebar.verify_dakota_contacts_tab_contact_detail_linkedin_url(
        Config.DAKOTA_CONTACTS_TAB_SEARCH_TERM
    )
