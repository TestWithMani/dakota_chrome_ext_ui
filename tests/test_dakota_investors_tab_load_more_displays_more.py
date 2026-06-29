import allure

from utils.config import Config


@allure.title("Verify Load More Investors displays more investors")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_investors_tab_load_more_displays_more(dakota_sidebar):
    """Open a company, load more investors, and verify additional investors appear."""
    dakota_sidebar.verify_dakota_investors_tab_load_more_displays_more(
        Config.DAKOTA_INVESTORS_TAB_SEARCH_TERM
    )
