import allure

from utils.config import Config


@allure.title("Verify Investment Details tab displays Geography")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investment_details_tab_geography(dakota_sidebar):
    """Open a Firm result and verify Investment Details displays Geography."""
    dakota_sidebar.verify_dakota_investment_details_tab_geography(
        Config.DAKOTA_INVESTMENT_DETAILS_TAB_SEARCH_TERM
    )
