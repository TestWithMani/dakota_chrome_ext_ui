import allure

from utils.config import Config


@allure.title("Verify all investors have their states/cities displayed")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investors_tab_investor_metro_areas(dakota_sidebar):
    """Open a company, scroll the Investors tab, and verify each investor has a state/city."""
    dakota_sidebar.verify_dakota_investors_tab_investor_metro_areas(
        Config.DAKOTA_INVESTORS_TAB_SEARCH_TERM
    )
