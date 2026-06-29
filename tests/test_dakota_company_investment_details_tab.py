import allure

from utils.config import Config


@allure.title("Verify firm has Investment Details tab")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_investment_details_tab(dakota_sidebar):
    """Open a Firm result and verify the Investment Details tab is available."""
    dakota_sidebar.verify_dakota_company_investment_details_tab(
        Config.DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM
    )
