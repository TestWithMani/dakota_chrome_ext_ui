import allure

from utils.config import Config


@allure.title("Verify Investors tab has Load More Investors button")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investors_tab_load_more_button(dakota_sidebar):
    """Open a company and verify Load More Investors is visible on the Investors tab."""
    dakota_sidebar.verify_dakota_investors_tab_load_more_button(
        Config.DAKOTA_INVESTORS_TAB_SEARCH_TERM
    )
