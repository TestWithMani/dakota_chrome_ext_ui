import allure

from utils.config import Config


@allure.title("Verify Dakota sidebar Load more displays additional results")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_search_load_more(dakota_sidebar):
    """Search, scroll to end, click Load more, and verify more results appear."""
    dakota_sidebar.verify_dakota_search_results_load_more(
        Config.DAKOTA_SIDEBAR_SEARCH_TERM
    )
