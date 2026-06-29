import allure

from utils.config import Config


@allure.title("Verify Investment Details tab displays Industry")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investment_details_tab_industry(dakota_sidebar):
    """Open a Firm result and verify Investment Details displays Industry."""
    dakota_sidebar.verify_dakota_investment_details_tab_industry(
        Config.DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM
    )
