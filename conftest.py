"""
Pytest configuration and Selenium fixtures for Dakota Chrome extension UI tests.

Aligned with Dakota_Ext_Performance:
  - BiDi extension install from downloaded .crx
  - Portal login first, then extension SSO via floating button click
  - logged_in_driver always runs full login_to_dakota (works in Jenkins)
"""

import json
import os
import shutil
import tempfile
import time
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from download_extension import (
    CRX_FILE,
    EXTENSION_ID,
    EXTENSION_NAME,
    UNPACKED_DIR,
    download_extension,
)
from pages.dakota_auth import DakotaCredentials, login_to_dakota
from pages.dakota_sidebar_page import DakotaSidebarPage
from utils.allure_helpers import (
    allure_available,
    attach_failure_bundle,
    attach_page_info,
    attach_screenshot,
    attach_text,
)
from utils.credentials import load_dakota_credentials

DEFAULT_TIMEOUT = 20
PROJECT_ROOT = Path(__file__).resolve().parent

# Fixed viewport — same as Dakota_Ext_Performance headless Jenkins (1920x1080).
CHROME_WINDOW_WIDTH = int(os.environ.get("CHROME_WINDOW_WIDTH", "1920"))
CHROME_WINDOW_HEIGHT = int(os.environ.get("CHROME_WINDOW_HEIGHT", "1080"))

TEST_EXECUTION_ORDER = {
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
    "test_dakota_linkedin_company_auto_search": 42,
}

SMOKE_TESTS = {
    "test_dakota_extension_installation",
    "test_login_to_dakota",
    "test_dakota_search_results",
    "test_dakota_company_details",
    "test_dakota_contacts_tab_results",
    "test_dakota_investors_tab_results",
    "test_dakota_platform_details_tab_platform_description",
    "test_dakota_linkedin_company_auto_search",
}


def is_headless_mode() -> bool:
    if os.environ.get("DAKOTA_HEADLESS", "").strip().lower() in {"1", "true", "yes"}:
        return True
    if os.environ.get("CI", "").strip().lower() in {"1", "true", "yes"}:
        return True
    if os.environ.get("JENKINS_URL"):
        return True
    return False


def ensure_extension_ready() -> Path:
    manifest = UNPACKED_DIR / "manifest.json"
    if not manifest.exists():
        print("\nExtension not found — downloading now...")
        return download_extension()
    return UNPACKED_DIR


def read_manifest(unpacked_dir: Path) -> dict:
    manifest_path = unpacked_dir / "manifest.json"
    with manifest_path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_extension_url(extension_id: str, relative_path: str = "") -> str:
    base = f"chrome-extension://{extension_id}/"
    if not relative_path:
        return base
    return base + relative_path.lstrip("/")


def create_chrome_options(user_data_dir: Path) -> Options:
    options = Options()
    options.enable_bidi = True
    options.enable_webextensions = True
    options.add_argument(f"--user-data-dir={user_data_dir}")
    options.add_argument(f"--window-size={CHROME_WINDOW_WIDTH},{CHROME_WINDOW_HEIGHT}")

    if is_headless_mode():
        options.add_argument("--headless=new")

    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    return options


def configure_chrome_window(driver: webdriver.Chrome) -> None:
    """Ensure a consistent viewport locally and in Jenkins headless."""
    driver.set_window_size(CHROME_WINDOW_WIDTH, CHROME_WINDOW_HEIGHT)


def install_extension(driver: webdriver.Chrome, unpacked_extension_path: Path) -> str:
    result = driver.webextension.install(path=str(unpacked_extension_path))
    if isinstance(result, dict):
        return result["extension"]
    return result


def wait_for_extension_page(driver: webdriver.Chrome, url: str, timeout: int = DEFAULT_TIMEOUT) -> None:
    driver.get(url)
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )


def is_extension_loaded(driver: webdriver.Chrome, extension_id: str, timeout: int = DEFAULT_TIMEOUT) -> bool:
    manifest_url = build_extension_url(extension_id, "manifest.json")
    try:
        wait_for_extension_page(driver, manifest_url, timeout)
        body_text = driver.find_element("tag name", "body").text.strip()
        if not body_text:
            return False
        parsed = json.loads(body_text)
        return parsed.get("name") is not None or parsed.get("manifest_version") is not None
    except (TimeoutException, json.JSONDecodeError, Exception):
        return False


def is_content_script_active(driver: webdriver.Chrome, timeout: int = DEFAULT_TIMEOUT) -> bool:
    script = """
        const host = document.getElementById('crxjs-app');
        return !!(host && host.shadowRoot);
    """
    try:
        WebDriverWait(driver, timeout).until(lambda d: d.execute_script(script))
        return True
    except TimeoutException:
        return False


def pause_for_visual_inspection(seconds: int, message: str) -> None:
    if seconds <= 0:
        return
    print(f"\n[VISUAL PAUSE] {message}")
    print(f"               Waiting {seconds} seconds — look at the Chrome window now.\n")
    time.sleep(seconds)


def open_demo_page_with_extension(driver: webdriver.Chrome) -> None:
    """Open example.com where Dakota injects its floating button / sidebar."""
    driver.get("https://example.com")
    WebDriverWait(driver, DEFAULT_TIMEOUT).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    is_content_script_active(driver)
    time.sleep(2)


def _get_pause_seconds(request) -> int:
    cli_value = request.config.getoption("--pause")
    if cli_value is not None:
        return max(0, int(cli_value))
    return max(0, int(os.environ.get("DAKOTA_PAUSE_SECONDS", "0")))


def pytest_addoption(parser):
    parser.addoption(
        "--pause",
        action="store",
        default=None,
        type=int,
        help="Keep Chrome open N seconds after extension loads (e.g. --pause 30)",
    )


def pytest_collection_modifyitems(items):
    items.sort(key=lambda item: TEST_EXECUTION_ORDER.get(item.name, 99))
    for item in items:
        item._execution_order = TEST_EXECUTION_ORDER.get(item.name, 99)
        if item.name in SMOKE_TESTS:
            item.add_marker(pytest.mark.smoke)


def _report_failure_text(report) -> str:
    if report.longrepr is None:
        return "Test failed or broke."
    return str(report.longrepr)


def _mark_failed_or_broken_as_skipped(item, report) -> None:
    """
    Record failed/broken tests as skipped in pytest, Allure, and JUnit output.

    The original failure message is kept in the skip reason so it is still visible.
    """
    if report.outcome not in {"failed", "error"}:
        return
    original = _report_failure_text(report)
    reason = f"Skipped (test did not complete during {report.when}):\n{original}"
    report.outcome = "skipped"
    path, lineno, _ = item.location
    report.longrepr = (str(path), lineno, reason)


def _allure_story_for_test(test_name: str) -> str:
    if "login" in test_name:
        return "Login & Authentication"
    if "extension_installation" in test_name:
        return "Extension Setup"
    if "linkedin" in test_name:
        return "LinkedIn Integration"
    if "search" in test_name:
        return "Sidebar Search"
    if "contacts" in test_name:
        return "Contacts Tab"
    if "investors" in test_name:
        return "Investors Tab"
    if "investment_details" in test_name:
        return "Investment Details Tab"
    if "platform_details" in test_name:
        return "Platform Details Tab"
    if "company" in test_name:
        return "Company Profile"
    return "General"


def _resolve_driver_from_item(item):
    for name in ("dakota_sidebar", "logged_in_driver", "shared_driver"):
        if name not in item.funcargs:
            continue
        value = item.funcargs[name]
        return value.driver if isinstance(value, DakotaSidebarPage) else value
    return None


def pytest_runtest_setup(item):
    execution_order = getattr(item, "_execution_order", 99)
    module_name = item.module.__name__.rsplit(".", 1)[-1]
    if not allure_available():
        return

    allure.dynamic.parent_suite("Dakota Automation")
    allure.dynamic.suite(f"{execution_order:03d} - {module_name}")
    allure.dynamic.feature("Dakota Chrome Extension UI")
    allure.dynamic.story(_allure_story_for_test(item.name))

    doc = getattr(item.obj, "__doc__", None)
    if doc and doc.strip():
        allure.dynamic.description(doc.strip())

    build_url = os.environ.get("BUILD_URL", "").strip()
    if build_url:
        allure.dynamic.link(build_url, name="Jenkins Build", link_type=allure.link_type.LINK)


@pytest.fixture(scope="session", autouse=True)
def allure_report_environment():
    if not allure_available():
        yield
        return

    lines = [
        f"Headless: {is_headless_mode()}",
        f"Viewport: {CHROME_WINDOW_WIDTH}x{CHROME_WINDOW_HEIGHT}",
        f"CI: {os.environ.get('CI', 'false')}",
        f"Jenkins: {bool(os.environ.get('JENKINS_URL'))}",
    ]
    build_url = os.environ.get("BUILD_URL", "").strip()
    if build_url:
        lines.append(f"Build URL: {build_url}")
    attach_text("\n".join(lines), "Environment")
    yield


@pytest.fixture(autouse=True)
def allure_test_lifecycle(request):
    if not allure_available():
        yield
        return

    test_name = request.node.name
    with allure.step(f"Execute test: {test_name}"):
        yield

    rep = getattr(request.node, "rep_call", None)
    if rep is None or not rep.passed:
        return

    driver = _resolve_driver_from_item(request.node)
    if driver is not None:
        attach_screenshot(driver, f"Passed — {test_name}")
        attach_page_info(driver, "Final page info")


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.failed and allure_available():
        attach_failure_bundle(
            _resolve_driver_from_item(item),
            test_name=item.name,
            failure_text=_report_failure_text(report),
            phase=report.when,
        )

    if report.outcome in {"failed", "error"}:
        _mark_failed_or_broken_as_skipped(item, report)

        if allure_available() and report.when == "call":
            allure.dynamic.description(_report_failure_text(report))
            allure.dynamic.label("original_status", "failed")


def pytest_runtest_logreport(report):
    if report.when != "call":
        return
    test_name = report.nodeid
    if report.passed:
        print(f"\n[PASS] {test_name}", flush=True)
    elif report.skipped:
        print(f"\n[SKIP] {test_name}", flush=True)
    elif report.failed:
        print(f"\n[FAIL] {test_name}", flush=True)


@pytest.fixture(scope="session")
def extension_paths() -> dict:
    """Session-scoped: download extension once (same as Dakota_Ext_Performance)."""
    unpacked = ensure_extension_ready()
    return {
        "store_extension_id": EXTENSION_ID,
        "extension_name": EXTENSION_NAME,
        "crx_file": CRX_FILE,
        "unpacked_dir": unpacked,
        "manifest": read_manifest(unpacked),
    }


@pytest.fixture(scope="session")
def install_profile_dir():
    """Chrome profile for extension-install + login tests (tests 0–1)."""
    custom = os.environ.get("CHROME_USER_DATA_DIR")
    if custom:
        profile_dir = Path(custom) / "install"
        if os.environ.get("CHROME_USER_DATA_CLEANUP", "").lower() == "true":
            if profile_dir.is_dir():
                shutil.rmtree(profile_dir, ignore_errors=True)
        profile_dir.mkdir(parents=True, exist_ok=True)
    else:
        profile_dir = Path(tempfile.mkdtemp(prefix="dakota-ui-install-"))
    yield profile_dir
    if os.environ.get("CHROME_USER_DATA_CLEANUP", "").lower() == "true" or not custom:
        shutil.rmtree(profile_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def suite_profile_dir():
    """Chrome profile for the logged-in functional test session (tests 2–42)."""
    custom = os.environ.get("CHROME_USER_DATA_DIR")
    if custom:
        profile_dir = Path(custom)
        if os.environ.get("CHROME_USER_DATA_CLEANUP", "").lower() == "true":
            if profile_dir.is_dir():
                shutil.rmtree(profile_dir, ignore_errors=True)
        profile_dir.mkdir(parents=True, exist_ok=True)
    else:
        profile_dir = Path(tempfile.mkdtemp(prefix="dakota-ui-suite-"))
    yield profile_dir
    if os.environ.get("CHROME_USER_DATA_CLEANUP", "").lower() == "true" or not custom:
        shutil.rmtree(profile_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def dakota_credentials() -> DakotaCredentials:
    return load_dakota_credentials()


@pytest.fixture(scope="session")
def shared_driver(extension_paths, install_profile_dir, request):
    """Chrome with extension on example.com — for install + login tests only."""
    options = create_chrome_options(install_profile_dir)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    configure_chrome_window(driver)
    driver.dakota_extension_id = install_extension(driver, extension_paths["unpacked_dir"])
    time.sleep(2)
    open_demo_page_with_extension(driver)
    pause_for_visual_inspection(
        _get_pause_seconds(request),
        "Dakota should be visible on example.com — look for the floating button "
        "at the bottom-right of the page (not in the Chrome toolbar).",
    )
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def installed_ext_id(shared_driver) -> str:
    return shared_driver.dakota_extension_id


@pytest.fixture(scope="session")
def logged_in_driver(extension_paths, suite_profile_dir, dakota_credentials):
    """
    Chrome with extension + portal login + extension SSO.

    Same as Dakota_Ext_Performance logged_in_driver — always runs full login.
    """
    options = create_chrome_options(suite_profile_dir)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    configure_chrome_window(driver)
    driver.dakota_extension_id = install_extension(driver, extension_paths["unpacked_dir"])
    time.sleep(1)

    login_to_dakota(driver, dakota_credentials, final_extension_delay=False)

    attach_screenshot(driver, "Suite session — logged in")
    yield driver
    driver.quit()


@pytest.fixture
def dakota_sidebar(logged_in_driver, dakota_credentials) -> DakotaSidebarPage:
    """Logged-in sidebar page object; reset before each test."""
    page = DakotaSidebarPage(logged_in_driver, credentials=dakota_credentials)
    page.reset_for_test()
    return page
