import allure

from utils.config import Config


@allure.title("Verify Investors tab shows number of investors displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investors_tab_investor_count(dakota_sidebar):
    """Open a company and verify the Investors tab shows the investor count label."""
    dakota_sidebar.verify_dakota_investors_tab_investor_count(
        Config.DAKOTA_INVESTORS_TAB_SEARCH_TERM
    )
