import allure

from conftest import is_content_script_active, is_extension_loaded, open_demo_page_with_extension
from utils.allure_helpers import allure_step


@allure.title("Verify Dakota extension is installed via WebDriver BiDi")
@allure.severity(allure.severity_level.CRITICAL)
def test_dakota_extension_installation(shared_driver, installed_ext_id):
    """
    Same as reference chrome_driver post-install checks:
    manifest readable + content script active on example.com.
    """
    with allure_step(shared_driver, "Verify extension manifest is readable after BiDi install"):
        assert is_extension_loaded(shared_driver, installed_ext_id), (
            "Dakota extension manifest was not readable after BiDi install."
        )

    with allure_step(shared_driver, "Verify Dakota content script injects on example.com"):
        open_demo_page_with_extension(shared_driver)
        assert is_content_script_active(shared_driver), (
            "Dakota content script did not inject on example.com."
        )
