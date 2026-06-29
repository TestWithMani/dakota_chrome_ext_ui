import allure

from utils.config import Config


@allure.title("Verify Dakota company General tab Account Overview")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_account_overview(dakota_sidebar):
    """Open a company and verify Account Overview is displayed on the General tab."""
    dakota_sidebar.verify_dakota_company_account_overview(
        Config.DAKOTA_COMPANY_DETAILS_SEARCH_TERM
    )
