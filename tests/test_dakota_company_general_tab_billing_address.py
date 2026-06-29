import allure

from utils.config import Config


@allure.title("Verify Dakota company General tab Billing Address")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_general_tab_billing_address(dakota_sidebar):
    """Open a company and verify Billing Address is displayed on the General tab."""
    dakota_sidebar.verify_dakota_company_general_tab_billing_address(
        Config.DAKOTA_COMPANY_DETAILS_SEARCH_TERM
    )
