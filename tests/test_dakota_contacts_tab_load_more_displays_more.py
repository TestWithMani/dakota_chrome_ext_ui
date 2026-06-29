import allure

from utils.config import Config


@allure.title("Verify Load more displays more contacts")
@allure.severity(allure.severity_level.NORMAL)
def test_dakota_contacts_tab_load_more_displays_more(dakota_sidebar):
    """Open a company, load more contacts, and verify additional contacts appear."""
    dakota_sidebar.verify_dakota_contacts_tab_load_more_displays_more(
        Config.DAKOTA_CONTACTS_LOAD_MORE_DISPLAY_SEARCH_TERM
    )
