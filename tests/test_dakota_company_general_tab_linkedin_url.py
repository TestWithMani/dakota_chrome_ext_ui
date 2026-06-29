import allure

from utils.config import Config


@allure.title("Verify Dakota company General tab LinkedIn Url")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_company_general_tab_linkedin_url(dakota_sidebar):
    """Open a company and verify LinkedIn Url is displayed on the General tab."""
    dakota_sidebar.verify_dakota_company_general_tab_linkedin_url(
        Config.DAKOTA_COMPANY_DETAILS_SEARCH_TERM
    )
