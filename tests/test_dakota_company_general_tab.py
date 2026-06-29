import allure

from utils.config import Config


@allure.title("Verify Dakota company General tab stat cards")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_general_tab(dakota_sidebar):
    """Open a company and verify Contacts, News, and AUM stat cards on General tab."""
    dakota_sidebar.verify_dakota_company_general_tab(
        Config.DAKOTA_COMPANY_DETAILS_SEARCH_TERM
    )
