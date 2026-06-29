import allure

from pages.dakota_auth import DAKOTA_PORTAL_URL, login_to_dakota
from utils.allure_helpers import allure_step


@allure.title("Login to Dakota - portal and extension SSO")
@allure.severity(allure.severity_level.NORMAL)
def test_login_to_dakota(shared_driver, dakota_credentials):
    """
    Same flow as Dakota_Ext_Performance test_dakota_portal_and_extension_login:
      1. Login on Dakota portal (username + password)
      2. Open extension sidebar via floating button
      3. Click Log in with Salesforce — SSO auto-authenticates
    """
    login_to_dakota(shared_driver, dakota_credentials)

    with allure_step(shared_driver, "Verify portal URL after login"):
        assert DAKOTA_PORTAL_URL.rstrip("/") in shared_driver.current_url.rstrip("/") or (
            "/dakotaMarketplace/s/" in shared_driver.current_url
        )

    with allure_step(shared_driver, "Verify company search is visible in extension sidebar"):
        search_placeholder = shared_driver.execute_script(
            """
            const host = document.getElementById('crxjs-app');
            const input = host?.shadowRoot?.querySelector('#company-search');
            return input ? input.placeholder : null;
            """
        )
        assert search_placeholder, "Company search should be visible after extension SSO login."
        print(f"\n  Portal URL : {shared_driver.current_url}")
        print(f"  Search box : {search_placeholder!r}")
