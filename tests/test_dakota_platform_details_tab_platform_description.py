import allure

from utils.config import Config


@allure.title("Verify Platform Details tab displays Platform Description")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_platform_details_tab_platform_description(dakota_sidebar):
    """Open a company and verify Platform Details displays Platform Description."""
    dakota_sidebar.verify_dakota_platform_details_tab_platform_description(
        Config.DAKOTA_PLATFORM_DETAILS_TAB_SEARCH_TERM
    )
