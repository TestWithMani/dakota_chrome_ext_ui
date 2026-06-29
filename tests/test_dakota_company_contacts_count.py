import allure

from utils.config import Config


@allure.title("Verify Contacts tab count matches General tab stat")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_contacts_count(dakota_sidebar):
    """Open a company and verify Contacts tab items match General tab Contacts count."""
    dakota_sidebar.verify_dakota_contacts_count_matches_general_tab(
        Config.DAKOTA_COMPANY_DETAILS_SEARCH_TERM
    )
