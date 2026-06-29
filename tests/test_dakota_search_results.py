import allure

from utils.config import Config


@allure.title("Verify Dakota sidebar search results")
@allure.severity(allure.severity_level.CRITICAL)
def test_dakota_search_results(dakota_sidebar):
    """Search in the Dakota extension sidebar and verify results are displayed."""
    dakota_sidebar.verify_dakota_search_results(
        Config.DAKOTA_SIDEBAR_SEARCH_TERM
    )
