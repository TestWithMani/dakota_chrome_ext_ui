import os
import shutil

import allure
import pytest
from playwright.sync_api import sync_playwright

from utils.config import Config

_CHROME_PROFILE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    ".chrome-profile",
)


def _should_reset_chrome_profile() -> bool:
    if os.getenv("CHROME_USER_DATA_CLEANUP", "false").lower() == "true":
        return True
    return bool(os.getenv("JENKINS_URL") or os.getenv("CI"))


def pytest_collection_modifyitems(items):
    """Run extension installation before login so the shared profile has the extension."""
    order = {
        "test_dakota_extension_installation": 0,
        "test_login_to_dakota": 1,
        "test_dakota_search_results": 2,
        "test_dakota_search_scroll": 3,
        "test_dakota_search_load_more": 4,
        "test_dakota_company_details": 5,
        "test_dakota_company_general_tab": 6,
        "test_dakota_company_contacts_count": 7,
        "test_dakota_company_account_overview": 8,
        "test_dakota_company_general_tab_type": 9,
        "test_dakota_company_general_tab_metro_area": 10,
        "test_dakota_company_general_tab_website": 11,
        "test_dakota_company_general_tab_linkedin_url": 12,
        "test_dakota_company_general_tab_billing_address": 13,
        "test_dakota_company_investors_tab": 14,
        "test_dakota_company_investment_details_tab": 15,
        "test_dakota_company_platform_details_tab": 16,
        "test_dakota_investors_tab_results": 17,
        "test_dakota_investors_tab_investor_count": 18,
        "test_dakota_investors_tab_load_more_button": 19,
        "test_dakota_investors_tab_load_more_displays_more": 20,
        "test_dakota_investors_tab_investor_metro_areas": 21,
        "test_dakota_investment_details_tab_details": 22,
        "test_dakota_investment_details_tab_geography": 23,
        "test_dakota_investment_details_tab_industry": 24,
        "test_dakota_investment_details_tab_check_size": 25,
        "test_dakota_platform_details_tab_platform_description": 26,
        "test_dakota_contacts_tab_results": 27,
        "test_dakota_contacts_tab_contact_count": 28,
        "test_dakota_contacts_tab_load_more_button": 29,
        "test_dakota_contacts_tab_load_more_displays_more": 30,
        "test_dakota_contacts_tab_contact_roles": 31,
        "test_dakota_contacts_tab_contact_urls": 32,
        "test_dakota_contacts_tab_contact_emails": 33,
        "test_dakota_contacts_tab_search_results": 34,
        "test_dakota_contacts_tab_contact_details": 35,
        "test_dakota_contacts_tab_contact_type": 36,
        "test_dakota_contacts_tab_contact_metro_area": 37,
        "test_dakota_contacts_tab_contact_phone": 38,
        "test_dakota_contacts_tab_contact_detail_email": 39,
        "test_dakota_contacts_tab_contact_detail_linkedin_url": 40,
        "test_dakota_contacts_tab_go_back_to_contact_list": 41,
    }
    items.sort(key=lambda item: order.get(item.name, 99))
    for item in items:
        item._execution_order = order.get(item.name, 99)


def pytest_runtest_setup(item):
    """Label each test in Allure so Suites view lists them in execution order."""
    execution_order = getattr(item, "_execution_order", 99)
    module_name = item.module.__name__.rsplit(".", 1)[-1]
    allure.dynamic.parent_suite("Dakota Automation")
    allure.dynamic.suite(f"{execution_order:03d} - {module_name}")


def pytest_runtest_logreport(report):
    """Print a clear pass/fail line to the console after each test."""
    if report.when != "call":
        return

    test_name = report.nodeid
    if report.passed:
        print(f"\n[PASS] {test_name}", flush=True)
    elif report.failed:
        print(f"\n[FAIL] {test_name}", flush=True)
    elif report.skipped:
        print(f"\n[SKIP] {test_name}", flush=True)


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def _user_data_dir():
    path = os.getenv("CHROME_USER_DATA_DIR", _CHROME_PROFILE_DIR)
    if _should_reset_chrome_profile() and os.path.isdir(path):
        shutil.rmtree(path, ignore_errors=True)
    os.makedirs(path, exist_ok=True)
    yield path
    if _should_reset_chrome_profile():
        shutil.rmtree(path, ignore_errors=True)


@pytest.fixture(scope="session")
def context(playwright_instance, _user_data_dir):
    browser_type = getattr(playwright_instance, Config.BROWSER)
    browser_args = []
    if Config.START_MAXIMIZED:
        browser_args.append("--start-maximized")

    launch_options = {
        "headless": Config.HEADLESS,
        "ignore_default_args": ["--disable-extensions"],
        "slow_mo": Config.SLOW_MO,
        "args": browser_args,
    }
    if Config.START_MAXIMIZED:
        launch_options["no_viewport"] = True
    else:
        launch_options["viewport"] = {
            "width": Config.VIEWPORT_WIDTH,
            "height": Config.VIEWPORT_HEIGHT,
        }

    if Config.BROWSER_CHANNEL:
        launch_options["channel"] = Config.BROWSER_CHANNEL

    context = browser_type.launch_persistent_context(
        _user_data_dir,
        **launch_options,
    )
    yield context
    context.close()


@pytest.fixture
def page(context):
    page = context.pages[0] if context.pages else context.new_page()
    yield page
    if not page.is_closed():
        page.close()


@pytest.fixture
def dakota_page(context):
    """New tab in the same persistent Chrome profile (extension remains available)."""
    dakota_tab = context.new_page()
    yield dakota_tab
    if not dakota_tab.is_closed():
        dakota_tab.close()
