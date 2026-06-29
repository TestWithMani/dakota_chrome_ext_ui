import allure

from utils.config import Config


@allure.title("Verify company details open from Dakota search result")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_details(dakota_sidebar):
    """Search, open a result, and verify company details are displayed."""
    dakota_sidebar.verify_dakota_company_details(
        Config.DAKOTA_COMPANY_DETAILS_SEARCH_TERM
    )
