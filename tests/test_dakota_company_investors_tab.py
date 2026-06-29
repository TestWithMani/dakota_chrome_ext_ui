import allure

from utils.config import Config


@allure.title("Verify private company has Investors tab")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_investors_tab(dakota_sidebar):
    """Open a private company and verify the Investors tab is available."""
    dakota_sidebar.verify_dakota_company_investors_tab(
        Config.DAKOTA_INVESTORS_TAB_SEARCH_TERM
    )
