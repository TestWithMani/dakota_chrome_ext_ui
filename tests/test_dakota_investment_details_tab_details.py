import allure

from utils.config import Config


@allure.title("Verify Investment Details tab displays details")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investment_details_tab_details(dakota_sidebar):
    """Open a Firm result and verify Investment Details shows data or empty state."""
    dakota_sidebar.verify_dakota_investment_details_tab_details(
        Config.DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM
    )
