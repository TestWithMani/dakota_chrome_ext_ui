import allure

from utils.config import Config


@allure.title("Verify allocator has Platform Details tab")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_platform_details_tab(dakota_sidebar):
    """Open an Allocator result and verify the Platform Details tab is available."""
    dakota_sidebar.verify_dakota_company_platform_details_tab(
        Config.DAKOTA_PLATFORM_DETAILS_TAB_SEARCH_TERM
    )
