import allure

from utils.config import Config


@allure.title("Verify Dakota sidebar auto-search from LinkedIn company page")
@allure.severity(allure.severity_level.CRITICAL)
def test_dakota_linkedin_company_auto_search(dakota_sidebar):
    """Open LinkedIn company page, open sidebar, and verify prefilled search results."""
    dakota_sidebar.verify_external_page_auto_search_results(
        Config.DAKOTA_EXTERNAL_PAGE_URL
    )
