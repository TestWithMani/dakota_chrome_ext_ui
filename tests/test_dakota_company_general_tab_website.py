import allure

from utils.config import Config


@allure.title("Verify Dakota company General tab Website")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_general_tab_website(dakota_sidebar):
    """Open a company and verify Website is displayed on the General tab."""
    dakota_sidebar.verify_dakota_company_general_tab_website(
        Config.DAKOTA_COMPANY_DETAILS_SEARCH_TERM
    )
