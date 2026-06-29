import allure

from utils.config import Config


@allure.title("Verify Investors tab displays results")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investors_tab_results(dakota_sidebar):
    """Open a company and verify the Investors tab shows investors or empty state."""
    dakota_sidebar.verify_dakota_investors_tab_results(
        Config.DAKOTA_INVESTORS_TAB_SEARCH_TERM
    )
