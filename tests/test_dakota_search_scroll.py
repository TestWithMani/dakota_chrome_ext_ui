import allure

from utils.config import Config


@allure.title("Verify Dakota sidebar search results scroll to end")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_search_scroll(dakota_sidebar):
    """Search in the Dakota sidebar and verify results can scroll to the end."""
    dakota_sidebar.verify_dakota_search_results_scroll(
        Config.DAKOTA_SIDEBAR_SEARCH_TERM
    )
