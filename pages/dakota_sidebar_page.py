"""Selenium page object for the Dakota Chrome extension sidebar (Shadow DOM)."""

from __future__ import annotations

import re
import time
from urllib.parse import parse_qs, unquote, urlparse

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.dakota_auth import (
    DAKOTA_PORTAL_URL,
    DakotaCredentials,
    _extension_search_ready,
    is_sidebar_open as auth_is_sidebar_open,
    open_dakota_sidebar,
    wait_for_extension_logged_in,
    wait_for_extension_on_page,
)
from pages.dakota_extension_actions import (
    DEFAULT_TIMEOUT,
    SEARCH_DEBOUNCE_SEC,
    DakotaExtensionActions,
)
from utils.allure_helpers import allure_step


class DakotaSidebarPage(DakotaExtensionActions):
    LOGIN_BUTTON_SELECTOR = ".dakota-salesforce-signin-button"
    SEARCH_BAR_SELECTOR = "input.dakota-search-input, #company-search"
    SEARCH_BAR_SELECTORS = (
        "input.dakota-search-input",
        "#company-search",
        "input[placeholder*='Search']",
        "input[aria-label*='Search']",
        "input",
    )
    SIDEBAR_OPEN_SELECTOR = ".dakota-sidebar-container.open"
    SIDEBAR_TOGGLE_SELECTOR = ".dakota-floating-button"
    SEARCH_RESULT_ITEM_SELECTOR = ".dakota-record-item"
    SEARCH_RESULT_NAME_SELECTOR = ".dakota-record-name"
    SEARCH_RESULT_TYPE_SELECTOR = ".dakota-record-type"
    ALLOCATOR_RECORD_TYPE_LABEL = "Allocator"
    LOAD_MORE_BUTTON_SELECTOR = "button.dakota-load-more-button"
    STATS_GRID_SELECTOR = ".dakota-stats-grid"
    STAT_ITEM_SELECTOR = ".dakota-stat-item"
    STAT_NUMBER_SELECTOR = ".dakota-stat-number"
    STAT_LABEL_SELECTOR = ".dakota-stat-label"
    GENERAL_TAB_STAT_LABELS = (
        "Contacts",
        "Recent News Mentions",
        "AUM",
    )
    CONTACTS_TAB_NAME = "Contacts"
    CONTACTS_TAB_SELECTOR = 'a.dakota-tab-button[href*="/contacts"]'
    CONTACTS_NO_RESULTS_TEXT = "No Results Found"
    CONTACTS_HEADER_SELECTOR = ".contacts-dakota-records-header"
    CONTACTS_COUNT_TEXT_PATTERN = re.compile(r"\(Showing \d+ results?\)", re.I)
    CONTACTS_PAGE_SIZE = 10
    LOAD_MORE_CONTACTS_BUTTON_TEXT = "Load more"
    CONTACTS_LOAD_MORE_BUTTON_SELECTOR = "button.contacts-dakota-load-more-button"
    CONTACTS_SCROLL_CONTAINER_SELECTORS = (
        ".contacts-dakota-sidebar-body",
        ".contacts-dakota-records-list",
        ".dakota-sidebar-body",
        ".dakota-loggedin-body",
        ".dakota-sidebar-content",
    )
    INVESTORS_TAB_NAME = "Investors"
    INVESTORS_TAB_SELECTOR = 'a.dakota-tab-button[href*="/investors"]'
    INVESTORS_NO_RESULTS_TEXT = "No Investors Found"
    INVESTOR_ITEM_SELECTOR = ".dakota-investor-item"
    INVESTOR_DETAILS_SELECTOR = ".dakota-investor-details"
    INVESTOR_METRO_SELECTOR = ".dakota-investor-metro"
    INVESTORS_HEADER_SELECTOR = ".dakota-investors-header"
    INVESTORS_COUNT_TEXT_PATTERN = re.compile(r"\(Showing \d+ investors?\)", re.I)
    LOAD_MORE_INVESTORS_BUTTON_TEXT = "Load More Investors"
    LOAD_MORE_INVESTORS_MAX_ATTEMPTS = 3
    INVESTORS_PAGE_SELECTOR = ".dakota-investors-page"
    INVESTORS_SCROLL_CONTAINER_SELECTORS = (
        ".dakota-investors-page",
        ".dakota-sidebar-body",
        ".dakota-loggedin-body",
        ".dakota-sidebar-content",
    )
    INVESTMENT_DETAILS_TAB_NAME = "Investment Details"
    INVESTMENT_DETAILS_TAB_SELECTOR = 'a.dakota-tab-button[href*="/investment-details"]'
    INVESTMENT_DETAILS_NO_CONTENT_TEXT = "No investment information available"
    INVESTMENT_DETAILS_ITEM_SELECTOR = ".dakota-investment-details-item"
    INVESTMENT_DETAILS_DESCRIPTION_SELECTOR = ".dakota-investment-description"
    INVESTMENT_DETAILS_GEOGRAPHY_LABEL = "Geography"
    INVESTMENT_DETAILS_INDUSTRY_LABEL = "Industry"
    INVESTMENT_DETAILS_CHECK_SIZE_LABEL = "Check Size"
    INVESTMENT_DETAILS_PAGE_SELECTOR = ".dakota-investment-details-page"
    PLATFORM_DETAILS_TAB_NAME = "Platform Details"
    PLATFORM_DETAILS_TAB_SELECTOR = 'a.dakota-tab-button[href*="/platform-details"]'
    PLATFORM_DETAILS_ITEM_SELECTOR = ".dakota-platform-info-item"
    PLATFORM_DETAILS_DESCRIPTION_SELECTOR = ".dakota-platform-description"
    PLATFORM_DETAILS_PLATFORM_DESCRIPTION_LABEL = "Platform Description"
    CONTACT_ITEM_SELECTOR = ".contacts-dakota-record-item"
    CONTACT_ROLE_SELECTOR = ".contacts-dakota-record-subDetails"
    CONTACT_URL_LINK_SELECTOR = "a.contacts-dakota-contact-link"
    CONTACT_EMAIL_SELECTOR = ".contacts-dakota-contact-email"
    CONTACT_EMAIL_LINK_SELECTOR = ".contacts-dakota-contact-email a.contacts-dakota-contact-link"
    CONTACTS_SEARCH_INPUT_SELECTOR = "#contact-search, .contacts-dakota-search-input"
    CONTACT_NAME_SELECTOR = ".contacts-dakota-record-name"
    CONTACT_DETAIL_PAGE_SELECTOR = ".contacts-dakota-detail-page"
    CONTACT_DETAIL_NAME_SELECTOR = ".contacts-dakota-detail-name"
    CONTACT_DETAIL_TITLE_SELECTOR = ".contacts-dakota-detail-title"
    CONTACT_DETAIL_FIELD_SELECTOR = ".contacts-dakota-detail-field"
    CONTACT_DETAIL_FIELD_LABEL_SELECTOR = ".contacts-dakota-detail-field-label"
    CONTACT_DETAIL_FIELD_VALUE_SELECTOR = ".contacts-dakota-detail-field-value"
    CONTACT_DETAIL_CONTACT_TYPE_LABEL = "Contact Type"
    CONTACT_DETAIL_METRO_AREA_LABEL = "Metro Area"
    CONTACT_DETAIL_PHONE_LABEL = "Phone"
    CONTACT_DETAIL_EMAIL_LABEL = "Email"
    CONTACT_DETAIL_LINKEDIN_URL_LABEL = "LinkedIn URL"
    CONTACT_DETAIL_BACK_BUTTON_SELECTOR = ".contacts-dakota-detail-back-button"
    CONTACT_DETAIL_BACK_BUTTON_TEXT = "Go back to contact list"
    ACCOUNT_OVERVIEW_HEADING = "Account Overview"
    INFO_LABEL_SELECTOR = ".dakota-info-label"
    INFO_VALUE_SELECTOR = ".dakota-info-value"
    TYPE_LABEL = "Type"
    METRO_AREA_LABEL = "Metro Area"
    WEBSITE_LABEL = "Website"
    LINKEDIN_URL_LABEL = "LinkedIn Url"
    BILLING_ADDRESS_LABEL = "Billing Address"
    GENERAL_TAB_SCROLL_CONTAINER_SELECTORS = (
        ".dakota-sidebar-body",
        ".dakota-loggedin-body",
        ".dakota-sidebar-content",
    )

    def __init__(
        self,
        driver: webdriver.Chrome,
        credentials: DakotaCredentials | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> None:
        super().__init__(driver)
        self.credentials = credentials
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    # ------------------------------------------------------------------
    # Shadow DOM helpers
    # ------------------------------------------------------------------

    def _js(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    def _root(self) -> str:
        return "const root = document.getElementById('crxjs-app')?.shadowRoot;"

    def _sidebar(self) -> bool:
        return bool(
            self._js(
                f"""
                {self._root()}
                return !!(root && root.querySelector('{self.SIDEBAR_OPEN_SELECTOR}'));
                """
            )
        )

    def _is_visible_in_shadow(self, css_selector: str) -> bool:
        return bool(
            self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return false;
                const el = root.querySelector(arguments[0]);
                if (!el) return false;
                const style = window.getComputedStyle(el);
                return style.display !== 'none' && style.visibility !== 'hidden'
                    && el.offsetParent !== null;
                """,
                css_selector,
            )
        )

    def _wait_visible(self, css_selector: str, timeout: int | None = None) -> None:
        WebDriverWait(self.driver, timeout or self.timeout).until(
            lambda d: self._is_visible_in_shadow(css_selector)
        )

    def _click_shadow(self, css_selector: str) -> None:
        clicked = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return false;
            const el = root.querySelector(arguments[0]);
            if (!el) return false;
            el.click();
            return true;
            """,
            css_selector,
        )
        if not clicked:
            raise TimeoutException(f"Could not click shadow element: {css_selector}")

    def _fill_shadow_input(self, css_selector: str, value: str) -> None:
        filled = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return false;
            const input = root.querySelector(arguments[0]);
            if (!input) return false;
            input.focus();
            input.value = arguments[1];
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
            """,
            css_selector,
            value,
        )
        if not filled:
            raise TimeoutException(f"Could not fill shadow input: {css_selector}")

    def _query_count(self, css_selector: str) -> int:
        count = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return 0;
            return root.querySelectorAll(arguments[0]).length;
            """,
            css_selector,
        )
        return int(count or 0)

    def _query_text(self, css_selector: str) -> str:
        text = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return '';
            const el = root.querySelector(arguments[0]);
            return el ? (el.textContent || '').trim() : '';
            """,
            css_selector,
        )
        return str(text or "")

    def _query_attr(self, css_selector: str, attr: str) -> str:
        value = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return '';
            const el = root.querySelector(arguments[0]);
            return el ? (el.getAttribute(arguments[1]) || '').trim() : '';
            """,
            css_selector,
            attr,
        )
        return str(value or "")

    def _query_input_value(self, css_selector: str) -> str:
        value = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return '';
            const el = root.querySelector(arguments[0]);
            return el ? (el.value || '').trim() : '';
            """,
            css_selector,
        )
        return str(value or "")

    def _query_all_texts(self, css_selector: str) -> list[str]:
        texts = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return [];
            return Array.from(root.querySelectorAll(arguments[0]))
                .map(el => (el.textContent || '').trim());
            """,
            css_selector,
        )
        return list(texts or [])

        scrolled = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return false;
            const selectors = arguments[0];
            for (const sel of selectors) {
                const container = root.querySelector(sel);
                if (container && container.scrollHeight > container.clientHeight + 1) {
                    container.scrollTop = container.scrollHeight;
                    return true;
                }
            }
            const anchor = root.querySelector('.dakota-record-item, .contacts-dakota-record-item, .dakota-investor-item');
            if (!anchor) return false;
            let node = anchor.parentElement;
            while (node) {
                if (node.scrollHeight > node.clientHeight + 1) {
                    node.scrollTop = node.scrollHeight;
                    return true;
                }
                node = node.parentElement;
            }
            return false;
            """,
            list(container_selectors),
        )
        if not scrolled:
            self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                const anchor = root?.querySelector('.dakota-record-item');
                if (!anchor) return;
                let node = anchor.parentElement;
                while (node) {
                    if (node.scrollHeight > node.clientHeight + 1) {
                        node.scrollTop = node.scrollHeight;
                        return;
                    }
                    node = node.parentElement;
                }
                """
            )

    def _read_scroll_metrics(self, container_selectors: tuple[str, ...]) -> dict[str, int]:
        metrics = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            const selectors = arguments[0];
            const read = (node) => ({
                scrollTop: node.scrollTop,
                scrollHeight: node.scrollHeight,
                clientHeight: node.clientHeight,
            });
            if (!root) return { scrollTop: 0, scrollHeight: 0, clientHeight: 0 };
            for (const sel of selectors) {
                const container = root.querySelector(sel);
                if (container && container.scrollHeight > container.clientHeight + 1) {
                    return read(container);
                }
            }
            const anchor = root.querySelector('.dakota-record-item, .contacts-dakota-record-item, .dakota-investor-item');
            if (!anchor) return { scrollTop: 0, scrollHeight: 0, clientHeight: 0 };
            let node = anchor.parentElement;
            while (node) {
                if (node.scrollHeight > node.clientHeight + 1) return read(node);
                node = node.parentElement;
            }
            return { scrollTop: 0, scrollHeight: 0, clientHeight: 0 };
            """,
            list(container_selectors),
        )
        return {
            "scrollTop": int(metrics.get("scrollTop", 0)),
            "scrollHeight": int(metrics.get("scrollHeight", 0)),
            "clientHeight": int(metrics.get("clientHeight", 0)),
        }

    def _verify_scrolled_to_end(
        self,
        scroll_before: dict[str, int],
        scroll_after: dict[str, int],
        context: str,
    ) -> None:
        scroll_height = scroll_after["scrollHeight"]
        client_height = scroll_after["clientHeight"]
        scroll_top = scroll_after["scrollTop"]
        if scroll_height <= client_height + 1:
            print(f"{context}: list is not scrollable; already fully visible.", flush=True)
            return
        at_bottom = scroll_top + client_height >= scroll_height - 2
        if not at_bottom:
            pytest.fail(
                f"{context} did not scroll to the end. "
                f"scrollTop={scroll_top}, clientHeight={client_height}, "
                f"scrollHeight={scroll_height}"
            )
        if scroll_top < scroll_before["scrollTop"]:
            pytest.fail(
                f"{context} scroll position moved upward unexpectedly. "
                f"before={scroll_before['scrollTop']}, after={scroll_top}"
            )
        print(f"{context} scrolled successfully to the end of the list.", flush=True)

    # ------------------------------------------------------------------
    # Setup / navigation
    # ------------------------------------------------------------------

    def is_sidebar_open(self) -> bool:
        return auth_is_sidebar_open(self.driver)

    def open_sidebar_if_closed(self) -> None:
        if self.is_sidebar_open():
            return
        open_dakota_sidebar(self.driver, timeout=self.timeout)

    def ensure_sidebar_ready(self) -> None:
        from pages.dakota_auth import (
            _extension_search_ready,
            is_sidebar_open,
            open_dakota_sidebar,
            wait_for_extension_logged_in,
            wait_for_extension_on_page,
        )

        if _extension_search_ready(self.driver):
            if not is_sidebar_open(self.driver):
                open_dakota_sidebar(self.driver, timeout=self.timeout)
            return

        wait_for_extension_on_page(self.driver, timeout=self.timeout)
        deadline = time.monotonic() + self.timeout
        while time.monotonic() < deadline:
            if _extension_search_ready(self.driver):
                return
            open_dakota_sidebar(self.driver, timeout=self.timeout)
            time.sleep(0.5)
        wait_for_extension_logged_in(self.driver, timeout=self.timeout)

    def reset_for_test(self, credentials: DakotaCredentials | None = None) -> None:
        from pages.dakota_auth import (
            ensure_logged_in_on_portal,
            is_sidebar_open,
            open_dakota_sidebar,
            wait_for_extension_logged_in,
        )
        from utils.credentials import load_dakota_credentials

        with allure_step(self.driver, "Reset browser state for test"):
            creds = credentials or self.credentials or load_dakota_credentials()
            self.driver.get(DAKOTA_PORTAL_URL)
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self._wait_shadow()
            ensure_logged_in_on_portal(self.driver, creds)
            if not is_sidebar_open(self.driver):
                open_dakota_sidebar(self.driver, timeout=self.timeout)
            wait_for_extension_logged_in(self.driver, timeout=self.timeout)

    def search_and_verify_results(self, search_term: str) -> None:
        with allure_step(self.driver, f"Search for '{search_term}' in the Dakota sidebar"):
            self.ensure_sidebar_ready()
            timing = self.search_company(search_term)
            assert timing.result_count >= 1, (
                f"Expected at least one search result for '{search_term}', got 0."
            )
        with allure_step(self.driver, "Verify search results are displayed in the sidebar"):
            self._verify_search_results_visible(search_term)

    def _verify_search_results_visible(self, search_term: str) -> None:
        self._wait_visible(self.SEARCH_RESULT_ITEM_SELECTOR)
        count = self._query_count(self.SEARCH_RESULT_ITEM_SELECTOR)
        assert count >= 1, f"Expected at least one search result for '{search_term}', got 0."
        self._wait_visible(self.SEARCH_RESULT_NAME_SELECTOR)

    def scroll_search_results_to_end(self, search_term: str) -> None:
        with allure_step(self.driver, "Scroll search results to the end of the list"):
            self._wait_visible(self.SEARCH_RESULT_ITEM_SELECTOR)
            result_count = self._query_count(self.SEARCH_RESULT_ITEM_SELECTOR)
            assert result_count >= 1, f"Expected search results before scrolling for '{search_term}'."
            scroll_before = self._read_scroll_metrics((".dakota-sidebar-body", ".dakota-loggedin-body"))
            if result_count > 1:
                self._js(
                    """
                    const root = document.getElementById('crxjs-app')?.shadowRoot;
                    const items = root?.querySelectorAll('.dakota-record-item') || [];
                    if (items.length) items[items.length - 1].scrollIntoView({ block: 'end' });
                    """
                )
            self._scroll_shadow_container_to_end((".dakota-sidebar-body", ".dakota-loggedin-body"))
            scroll_after = self._read_scroll_metrics((".dakota-sidebar-body", ".dakota-loggedin-body"))
        with allure_step(self.driver, "Verify search results scrolled to the end"):
            self._verify_scrolled_to_end(scroll_before, scroll_after, "Search results")

    def load_more_search_results(self, search_term: str) -> None:
        with allure_step(self.driver, 'Click "Load more" to fetch additional search results'):
            count_before = self._query_count(self.SEARCH_RESULT_ITEM_SELECTOR)
            assert count_before >= 1, f"Expected search results before Load more for '{search_term}'."
            self.scroll_and_click_load_more()
            count_after = self._query_count(self.SEARCH_RESULT_ITEM_SELECTOR)
            assert count_after > count_before, (
                f'Expected more results after clicking "Load more" for '
                f"'{search_term}', but count stayed at {count_after}."
            )

    def open_first_search_result(self) -> None:
        with allure_step(self.driver, "Open the first search result"):
            self._wait_visible(self.SEARCH_RESULT_ITEM_SELECTOR)
            self.click_first_search_result()
            self.wait_for_company_detail()
            self._ensure_general_tab_visible()

    def open_search_result_for_tab(self, expected_tab: str) -> tuple[str, str]:
        """Open a search result whose company type maps to the expected profile tab."""
        from utils.company_types import profile_tab_for_company_type

        with allure_step(self.driver, f"Open search result for tab '{expected_tab}'"):
            self._wait_visible(self.SEARCH_RESULT_ITEM_SELECTOR)
            results = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return [];
                return Array.from(root.querySelectorAll('.dakota-record-item')).map((item) => {
                    const name = item.querySelector('.dakota-record-name, .dakota-record-title');
                    const typeEl = item.querySelector(
                        '.dakota-record-type p, .dakota-record-type'
                    );
                    return {
                        name: (name?.textContent || '').trim(),
                        type: (typeEl?.textContent || '').trim(),
                    };
                });
                """
            )
            assert results, "No search results found to open."

            for index, row in enumerate(results):
                ctype = row.get("type", "")
                if profile_tab_for_company_type(ctype) != expected_tab:
                    continue
                clicked = self._js(
                    """
                    const root = document.getElementById('crxjs-app')?.shadowRoot;
                    const items = root?.querySelectorAll('.dakota-record-item') || [];
                    const item = items[arguments[0]];
                    if (!item) return false;
                    item.click();
                    return true;
                    """,
                    index,
                )
                if not clicked:
                    continue
                name = row.get("name", "")
                self.wait_for_company_detail()
                self._ensure_general_tab_visible()
                print(
                    f"Opened '{name}' ({ctype}) for tab '{expected_tab}'.",
                    flush=True,
                )
                return name, ctype

            available = ", ".join(
                f"{r.get('name', '?')} [{r.get('type', '?')}]" for r in results[:5]
            )
            pytest.fail(
                f"No search result maps to tab '{expected_tab}'. "
                f"Results: {available}"
            )

    def _ensure_general_tab_visible(self) -> None:
        """Company detail defaults to General; scroll stats into view after load."""
        self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            const body = root?.querySelector('.dakota-sidebar-body, .dakota-loggedin-body');
            if (body) body.scrollTop = 0;
            const grid = root?.querySelector('.dakota-stats-grid');
            if (grid) grid.scrollIntoView({ block: 'start' });
            """
        )
        time.sleep(0.5)

    def open_allocator_search_result(self) -> None:
        self._open_search_result_by_types(self.ALLOCATOR_RECORD_TYPE_LABEL)

    def _open_search_result_by_types(self, *type_labels: str) -> None:
        with allure_step(self.driver, f"Open search result with type {type_labels!r}"):
            self._wait_visible(self.SEARCH_RESULT_ITEM_SELECTOR)
            normalized = [label.strip().casefold() for label in type_labels]
            clicked = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return false;
                const targets = arguments[0];
                const items = root.querySelectorAll('.dakota-record-item');
                for (const item of items) {
                    const typeEl = item.querySelector(
                        '.dakota-record-type p, .dakota-record-type'
                    );
                    const typeText = (typeEl?.textContent || '').trim().toLowerCase();
                    if (!targets.includes(typeText)) continue;
                    item.click();
                    return true;
                }
                return false;
                """,
                normalized,
            )
            if not clicked:
                pytest.fail(
                    f"No search result found for type(s) {type_labels!r}."
                )
            self.wait_for_company_detail()
            self._ensure_general_tab_visible()

    def open_search_result_and_verify_company_details(self, search_term: str) -> None:
        self.open_first_search_result()
        with allure_step(self.driver, "Verify company details content is displayed"):
            self._verify_company_details_content_displayed(search_term)

    def _verify_company_details_content_displayed(self, search_term: str) -> None:
        def _has_content(_driver):
            length = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return 0;
                const sidebar = root.querySelector('.dakota-sidebar-container.open');
                return sidebar ? (sidebar.innerText || '').trim().length : 0;
                """
            )
            return length if length and length >= 30 else None

        try:
            WebDriverWait(self.driver, self.timeout).until(_has_content)
        except TimeoutException:
            pytest.fail(
                "No company details content was displayed in the sidebar after "
                f"opening a search result for '{search_term}'."
            )

    # ------------------------------------------------------------------
    # LinkedIn / external page
    # ------------------------------------------------------------------

    @staticmethod
    def _is_linkedin_url(url: str) -> bool:
        return "linkedin.com" in url.lower()

    @staticmethod
    def _is_linkedin_authwall(url: str) -> bool:
        return "linkedin.com/authwall" in url.lower()

    def _clear_linkedin_cookies(self) -> None:
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            if "linkedin.com" in cookie.get("domain", "").lower():
                self.driver.delete_cookie(cookie["name"])

    @staticmethod
    def _extract_session_redirect(url: str) -> str | None:
        params = parse_qs(urlparse(url).query)
        redirects = params.get("sessionRedirect", [])
        if not redirects:
            return None
        return unquote(redirects[0])

    def _dismiss_linkedin_prompts(self) -> None:
        if "linkedin.com" not in self.driver.current_url.lower():
            return
        selectors = [
            "button[aria-label='Dismiss']",
            "button.artdeco-modal__dismiss",
        ]
        for css in selectors:
            try:
                buttons = self.driver.find_elements(By.CSS_SELECTOR, css)
                for btn in buttons:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(0.5)
                        return
            except Exception:
                continue

    def _open_linkedin_public_page(self, target_url: str) -> None:
        normalized_target = target_url.rstrip("/")
        self._clear_linkedin_cookies()
        self.driver.get(target_url)
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(SEARCH_DEBOUNCE_SEC)
        self._dismiss_linkedin_prompts()

        if self._is_linkedin_authwall(self.driver.current_url):
            redirect_target = self._extract_session_redirect(self.driver.current_url) or target_url
            self._clear_linkedin_cookies()
            self.driver.get(redirect_target)
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            time.sleep(SEARCH_DEBOUNCE_SEC)
            self._dismiss_linkedin_prompts()

        if self._is_linkedin_authwall(self.driver.current_url):
            pytest.fail(
                "LinkedIn redirected to the authentication wall instead of the public "
                f"company page. Target URL: {target_url}."
            )

        WebDriverWait(self.driver, self.timeout).until(
            lambda d: re.search(
                re.escape(normalized_target) + r"/?", d.current_url, re.I
            )
        )

    def open_external_page_and_sidebar(self, page_url: str) -> None:
        normalized_url = page_url.rstrip("/")
        with allure_step(self.driver, f"Open external page: {page_url}"):
            if self._is_linkedin_url(page_url):
                self._open_linkedin_public_page(page_url)
            else:
                self.driver.get(page_url)
                WebDriverWait(self.driver, self.timeout).until(
                    lambda d: re.search(
                        re.escape(normalized_url) + r"/?", d.current_url, re.I
                    )
                )
        with allure_step(self.driver, "Open Dakota sidebar via floating button"):
            wait_for_extension_on_page(self.driver, timeout=self.timeout)
            open_dakota_sidebar(self.driver, timeout=self.timeout)

    @staticmethod
    def _normalize_url_for_search_prefill(url: str) -> str:
        normalized = url.strip()
        normalized = re.sub(r"^https?://", "", normalized, flags=re.I)
        normalized = re.sub(r"^www\.", "", normalized, flags=re.I)
        return normalized.rstrip("/")

    def verify_sidebar_prefilled_search_and_results(self, page_url: str) -> None:
        expected_prefill = self._normalize_url_for_search_prefill(page_url)
        with allure_step(
            self.driver,
            f"Verify sidebar search bar is prefilled with '{expected_prefill}'",
        ):
            self.ensure_sidebar_ready()
            self._wait_for_search_bar_url(page_url)
            actual_value = self._get_search_input_value()
            print(
                f"Sidebar search bar value: '{actual_value}' (expected '{expected_prefill}')",
                flush=True,
            )
        with allure_step(self.driver, f"Verify search results for '{expected_prefill}'"):
            self._verify_search_results_visible(expected_prefill)

    def _get_search_input_value(self) -> str:
        for selector in self.SEARCH_BAR_SELECTORS:
            value = self._query_input_value(selector.split(",")[0].strip())
            if value:
                return value
        return self._query_input_value("#company-search")

    def _wait_for_search_bar_url(self, page_url: str, timeout_s: float | None = None) -> None:
        wait = timeout_s if timeout_s is not None else self.timeout
        expected = self._normalize_url_for_search_prefill(page_url)
        deadline = time.monotonic() + wait
        while time.monotonic() < deadline:
            actual = self._get_search_input_value()
            if self._normalize_url_for_search_prefill(actual) == expected:
                return
            time.sleep(0.5)
        actual = self._get_search_input_value()
        pytest.fail(
            "Sidebar search bar was not prefilled with the expected page URL. "
            f"Expected '{expected}', got '{actual}'."
        )


    # ------------------------------------------------------------------
    # General tab verifications
    # ------------------------------------------------------------------

    def _get_general_tab_stat_value(self, label: str) -> str:
        value = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return '';
            const target = arguments[0].trim().toLowerCase();
            const items = root.querySelectorAll('.dakota-stat-item');
            for (const item of items) {
                const lbl = item.querySelector('.dakota-stat-label');
                const labelText = (lbl?.textContent || item.textContent || '').trim().toLowerCase();
                if (!labelText.includes(target) && !(target === 'contacts' && labelText.includes('contact'))) {
                    continue;
                }
                item.scrollIntoView({ block: 'center' });
                const num = item.querySelector('.dakota-stat-number');
                return num ? (num.textContent || '').trim() : '';
            }
            return '';
            """,
            label,
        )
        if not value:
            pytest.fail(f"Expected a displayed count for {label}.")
        return str(value)

    def _get_general_tab_info_value(self, label: str) -> str:
        value = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return '';
            const labels = root.querySelectorAll('.dakota-info-label');
            for (const lbl of labels) {
                if ((lbl.textContent || '').trim() === arguments[0]) {
                    const val = lbl.nextElementSibling;
                    if (val && val.classList.contains('dakota-info-value')) {
                        return (val.textContent || '').trim();
                    }
                    const parent = lbl.parentElement;
                    const valueEl = parent?.querySelector('.dakota-info-value');
                    return valueEl ? (valueEl.textContent || '').trim() : '';
                }
            }
            return '';
            """,
            label,
        )
        return str(value or "")

    def _ensure_general_tab_info_label_visible(self, label: str) -> None:
        self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return;
            const labels = root.querySelectorAll('.dakota-info-label');
            let target = null;
            for (const lbl of labels) {
                if ((lbl.textContent || '').trim() === arguments[0]) {
                    target = lbl;
                    break;
                }
            }
            if (!target) return;
            const isScrollable = (el) => {
                const style = window.getComputedStyle(el);
                return (style.overflowY === 'auto' || style.overflowY === 'scroll')
                    && el.scrollHeight > el.clientHeight + 1;
            };
            for (let i = 0; i < 60; i++) {
                target.scrollIntoView({ block: 'center', inline: 'nearest' });
                const rect = target.getBoundingClientRect();
                let container = target.parentElement;
                while (container) {
                    if (isScrollable(container)) {
                        const cRect = container.getBoundingClientRect();
                        if (rect.top >= cRect.top && rect.bottom <= cRect.bottom) return;
                        if (rect.bottom > cRect.bottom) {
                            container.scrollTop += rect.bottom - cRect.bottom + 24;
                        } else {
                            container.scrollTop += 300;
                        }
                        break;
                    }
                    container = container.parentElement;
                }
            }
            """,
            label,
        )
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: bool(self._get_general_tab_info_value(label))
            or self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                const labels = root?.querySelectorAll('.dakota-info-label') || [];
                for (const lbl of labels) {
                    if ((lbl.textContent || '').trim() === arguments[0]) {
                        const rect = lbl.getBoundingClientRect();
                        return rect.width > 0 && rect.height > 0;
                    }
                }
                return false;
                """,
                label,
            )
        )

    def verify_general_tab_stat_cards(self) -> None:
        with allure_step(self.driver, "Verify General tab stat cards are displayed"):
            self._wait_visible(self.STATS_GRID_SELECTOR)
            for label in self.GENERAL_TAB_STAT_LABELS:
                stat_value = self._get_general_tab_stat_value(label)
                assert stat_value, f"Expected a displayed count for {label}."
                print(f"General tab {label}: {stat_value}", flush=True)

    def verify_general_tab_account_overview(self) -> None:
        with allure_step(self.driver, "Verify Account Overview heading is displayed"):
            self._wait_visible("h3")
            headings = self._query_all_texts("h3")
            assert any("Account Overview" in h for h in headings), (
                "Account Overview heading not found."
            )
        with allure_step(self.driver, "Verify Account Overview content is displayed"):
            content = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return '';
                const headings = root.querySelectorAll('h3');
                for (const h of headings) {
                    if (/Account Overview/i.test(h.textContent || '')) {
                        let sib = h.nextElementSibling;
                        while (sib) {
                            if (sib.tagName === 'P') return (sib.textContent || '').trim();
                            sib = sib.nextElementSibling;
                        }
                    }
                }
                return '';
                """
            )
            content_text = str(content or "").strip()
            assert len(content_text) >= 20, (
                "Account Overview section did not display meaningful content."
            )
            print(f"Account Overview displayed ({len(content_text)} characters)", flush=True)

    def verify_general_tab_type(self) -> None:
        with allure_step(self.driver, "Verify Type label is displayed on General tab"):
            self._wait_visible(self.INFO_LABEL_SELECTOR)
        with allure_step(self.driver, "Verify Type value is displayed on General tab"):
            type_value = self._get_general_tab_info_value(self.TYPE_LABEL)
            assert type_value, "Expected a displayed Type value on the General tab."
            print(f"General tab Type: {type_value}", flush=True)

    def verify_general_tab_metro_area(self) -> None:
        with allure_step(self.driver, "Verify Metro Area label is displayed on General tab"):
            self._wait_visible(self.INFO_LABEL_SELECTOR)
        with allure_step(self.driver, "Verify Metro Area value is displayed on General tab"):
            value = self._get_general_tab_info_value(self.METRO_AREA_LABEL)
            assert value, "Expected a displayed Metro Area value on the General tab."
            print(f"General tab Metro Area: {value}", flush=True)

    def verify_general_tab_website(self) -> None:
        with allure_step(self.driver, "Scroll General tab until Website is visible"):
            self._ensure_general_tab_info_label_visible(self.WEBSITE_LABEL)
        with allure_step(self.driver, "Verify Website value is displayed on General tab"):
            value = self._get_general_tab_info_value(self.WEBSITE_LABEL)
            assert value, "Expected a displayed Website value on the General tab."
            print(f"General tab Website: {value}", flush=True)

    def verify_general_tab_linkedin_url(self) -> None:
        with allure_step(self.driver, "Scroll General tab until LinkedIn Url is visible"):
            self._ensure_general_tab_info_label_visible(self.LINKEDIN_URL_LABEL)
        with allure_step(self.driver, "Verify LinkedIn Url value is displayed on General tab"):
            value = self._get_general_tab_info_value(self.LINKEDIN_URL_LABEL)
            assert value, "Expected a displayed LinkedIn Url value on the General tab."
            print(f"General tab LinkedIn Url: {value}", flush=True)

    def verify_general_tab_billing_address(self) -> None:
        with allure_step(self.driver, "Scroll General tab until Billing Address is visible"):
            self._ensure_general_tab_info_label_visible(self.BILLING_ADDRESS_LABEL)
        with allure_step(self.driver, "Verify Billing Address value is displayed on General tab"):
            value = self._get_general_tab_info_value(self.BILLING_ADDRESS_LABEL)
            assert value, "Expected a displayed Billing Address value on the General tab."
            print(f"General tab Billing Address: {value}", flush=True)

    def _parse_contacts_stat_count(self, value: str) -> int:
        normalized = value.strip().upper()
        if normalized == "N/A":
            pytest.fail(
                "General tab Contacts count is N/A; cannot compare with Contacts tab."
            )
        digits = re.sub(r"[^0-9]", "", value)
        if not digits:
            pytest.fail(f"Could not parse Contacts count from General tab value '{value}'.")
        return int(digits)

    # ------------------------------------------------------------------
    # Investors tab
    # ------------------------------------------------------------------

    def _open_investors_tab(self) -> None:
        self.click_tab_by_name(self.INVESTORS_TAB_NAME)
        self.wait_for_investors_tab_ready()
        print(f"Navigated to {self.INVESTORS_TAB_NAME} tab.", flush=True)

    def verify_company_investors_tab(self) -> None:
        with allure_step(self.driver, "Verify Investors tab is displayed"):
            self._wait_visible(self.INVESTORS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investors tab"):
            self._open_investors_tab()

    def verify_investors_tab_results(self) -> None:
        with allure_step(self.driver, "Verify Investors tab is displayed"):
            self._wait_visible(self.INVESTORS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investors tab"):
            self._open_investors_tab()
        with allure_step(self.driver, "Verify Investors tab displays results or empty state"):
            self._verify_investors_tab_content_displayed()

    def _verify_investors_tab_content_displayed(self) -> None:
        def _ready(_driver):
            if self._query_count(self.INVESTOR_ITEM_SELECTOR) > 0:
                return True
            texts = self._query_all_texts(".dakota-no-results p")
            return any(self.INVESTORS_NO_RESULTS_TEXT.lower() in t.lower() for t in texts)

        WebDriverWait(self.driver, self.timeout).until(_ready)
        if self._query_count(self.INVESTOR_ITEM_SELECTOR) == 0:
            print(
                f"Investors tab displayed empty state: {self.INVESTORS_NO_RESULTS_TEXT}",
                flush=True,
            )
        else:
            count = self._query_count(self.INVESTOR_ITEM_SELECTOR)
            print(f"Investors tab displayed {count} investor result(s).", flush=True)

    def verify_investors_tab_investor_count(self) -> None:
        with allure_step(self.driver, "Verify Investors tab is displayed"):
            self._wait_visible(self.INVESTORS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investors tab"):
            self._open_investors_tab()
        with allure_step(self.driver, "Verify Investors tab shows number of investors displayed"):
            self._verify_investors_tab_count_displayed()

    def _verify_investors_tab_count_displayed(self) -> None:
        header_text = self._query_text(self.INVESTORS_HEADER_SELECTOR)
        assert self.INVESTORS_TAB_NAME in header_text, "Investors header not found."
        match = re.search(r"Showing (\d+)", header_text, re.I)
        assert match, f"Could not parse investor count from '{header_text}'."
        displayed_count = int(match.group(1))
        print(f"Investors tab count label: {header_text}", flush=True)
        self._wait_visible(self.INVESTOR_ITEM_SELECTOR)
        assert self._query_count(self.INVESTOR_ITEM_SELECTOR) == displayed_count, (
            "Investors tab count label does not match displayed investor results."
        )

    def verify_investors_tab_load_more_button(self) -> None:
        with allure_step(self.driver, "Verify Investors tab is displayed"):
            self._wait_visible(self.INVESTORS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investors tab"):
            self._open_investors_tab()
        with allure_step(self.driver, "Scroll Investors tab until Load More Investors is visible"):
            self._ensure_load_more_investors_button_visible()
            print(f"{self.LOAD_MORE_INVESTORS_BUTTON_TEXT} button is visible.", flush=True)

    def verify_investors_tab_load_more_displays_more(self) -> None:
        with allure_step(self.driver, "Verify Investors tab is displayed"):
            self._wait_visible(self.INVESTORS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investors tab"):
            self._open_investors_tab()
        with allure_step(self.driver, "Scroll Investors tab until Load More Investors is visible"):
            self._ensure_load_more_investors_button_visible()
        with allure_step(self.driver, 'Click "Load More Investors" to fetch additional investors'):
            self._load_more_investors()
        with allure_step(self.driver, "Scroll Investors tab to the end of the list"):
            self.scroll_investors_tab_to_end()

    def verify_investors_tab_investor_metro_areas(self) -> None:
        with allure_step(self.driver, "Verify Investors tab is displayed"):
            self._wait_visible(self.INVESTORS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investors tab"):
            self._open_investors_tab()
        with allure_step(self.driver, "Scroll Investors tab until Load More Investors is visible"):
            self._ensure_load_more_investors_button_visible()
        with allure_step(self.driver, "Verify all investors on the page display a state/city"):
            self._verify_investors_metro_areas_displayed()

    def _verify_investors_metro_areas_displayed(self) -> None:
        self._wait_visible(self.INVESTOR_ITEM_SELECTOR)
        metros = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return [];
            return Array.from(root.querySelectorAll('.dakota-investor-item')).map(item => {
                const metro = item.querySelector('.dakota-investor-details .dakota-investor-metro, .dakota-investor-metro');
                return metro ? (metro.textContent || '').trim() : '';
            });
            """
        )
        assert metros and len(metros) >= 1, (
            "Expected at least one investor to verify state/city display."
        )
        for index, metro_text in enumerate(metros, start=1):
            assert metro_text, f"Investor {index} of {len(metros)} is missing a state/city."
            print(f"Investor {index} state/city: {metro_text}", flush=True)
        print(f"All {len(metros)} investor(s) display a state/city.", flush=True)

    def _load_more_investors_button_visible(self) -> bool:
        return bool(
            self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return false;
                const buttons = root.querySelectorAll('button');
                for (const btn of buttons) {
                    if (/load more investors/i.test((btn.textContent || '').trim())) {
                        return btn.offsetParent !== null;
                    }
                }
                return false;
                """
            )
        )

    def _ensure_load_more_investors_button_visible(self) -> None:
        for _ in range(60):
            if self._load_more_investors_button_visible():
                return
            self._scroll_shadow_container_to_end(self.INVESTORS_SCROLL_CONTAINER_SELECTORS)
            time.sleep(0.2)
        if not self._load_more_investors_button_visible():
            pytest.fail(
                f"{self.LOAD_MORE_INVESTORS_BUTTON_TEXT} button is not visible "
                "in the Investors tab viewport after scrolling."
            )

    def _load_more_investors(self) -> None:
        count_before = self._query_count(self.INVESTOR_ITEM_SELECTOR)
        assert count_before >= 1, (
            f"Expected investors before {self.LOAD_MORE_INVESTORS_BUTTON_TEXT}."
        )
        for attempt in range(1, self.LOAD_MORE_INVESTORS_MAX_ATTEMPTS + 1):
            self._ensure_load_more_investors_button_visible()
            clicked = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return false;
                const buttons = root.querySelectorAll('button');
                for (const btn of buttons) {
                    if (/load more investors/i.test((btn.textContent || '').trim())) {
                        btn.scrollIntoView({ block: 'center' });
                        btn.click();
                        return true;
                    }
                }
                return false;
                """
            )
            if not clicked:
                if attempt == self.LOAD_MORE_INVESTORS_MAX_ATTEMPTS:
                    pytest.fail(f"{self.LOAD_MORE_INVESTORS_BUTTON_TEXT} button not found.")
                continue

            try:
                WebDriverWait(self.driver, self.timeout).until(
                    lambda d: self._query_count(self.INVESTOR_ITEM_SELECTOR) > count_before
                )
                return
            except TimeoutException:
                if attempt == self.LOAD_MORE_INVESTORS_MAX_ATTEMPTS:
                    raise
                # Sometimes the first click is swallowed by the UI while list rerenders.
                self._scroll_shadow_container_to_end(self.INVESTORS_SCROLL_CONTAINER_SELECTORS)
                time.sleep(0.8)

    def scroll_investors_tab_to_end(self) -> None:
        self._wait_visible(self.INVESTOR_ITEM_SELECTOR)
        count = self._query_count(self.INVESTOR_ITEM_SELECTOR)
        assert count >= 1, "Expected investors before scrolling Investors tab."
        scroll_before = self._read_scroll_metrics(self.INVESTORS_SCROLL_CONTAINER_SELECTORS)
        if count > 1:
            self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                const items = root?.querySelectorAll('.dakota-investor-item') || [];
                if (items.length) items[items.length - 1].scrollIntoView({ block: 'end' });
                """
            )
        self._scroll_shadow_container_to_end(self.INVESTORS_SCROLL_CONTAINER_SELECTORS)
        scroll_after = self._read_scroll_metrics(self.INVESTORS_SCROLL_CONTAINER_SELECTORS)
        self._verify_scrolled_to_end(scroll_before, scroll_after, "Investors tab")

    # ------------------------------------------------------------------
    # Investment details tab
    # ------------------------------------------------------------------

    def _open_investment_details_tab(self) -> None:
        self._wait_visible(self.INVESTMENT_DETAILS_TAB_SELECTOR)
        self._click_shadow('a.dakota-tab-button[href*="/investment-details"]')
        time.sleep(1.5)
        print(f"Navigated to {self.INVESTMENT_DETAILS_TAB_NAME} tab.", flush=True)

    def verify_company_investment_details_tab(self) -> None:
        with allure_step(self.driver, "Verify Investment Details tab is displayed"):
            self._wait_visible(self.INVESTMENT_DETAILS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investment Details tab"):
            self._open_investment_details_tab()

    def verify_investment_details_tab_details(self) -> None:
        with allure_step(self.driver, "Verify Investment Details tab is displayed"):
            self._wait_visible(self.INVESTMENT_DETAILS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investment Details tab"):
            self._open_investment_details_tab()
        with allure_step(self.driver, "Verify Investment Details tab displays data or empty state"):
            self._verify_investment_details_tab_content_displayed()

    def _verify_investment_details_tab_content_displayed(self) -> None:
        def _ready(_driver):
            if self._query_count(self.INVESTMENT_DETAILS_ITEM_SELECTOR) > 0:
                return True
            texts = self._query_all_texts(".dakota-no-content p")
            return any(
                self.INVESTMENT_DETAILS_NO_CONTENT_TEXT.lower() in t.lower() for t in texts
            )

        WebDriverWait(self.driver, self.timeout).until(_ready)
        if self._query_count(self.INVESTMENT_DETAILS_ITEM_SELECTOR) == 0:
            print(
                "Investment Details tab displayed empty state: "
                f"{self.INVESTMENT_DETAILS_NO_CONTENT_TEXT}",
                flush=True,
            )
        else:
            count = self._query_count(self.INVESTMENT_DETAILS_ITEM_SELECTOR)
            print(f"Investment Details tab displayed {count} detail item(s).", flush=True)

    def _verify_investment_details_field(self, label: str) -> None:
        text = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return '';
            const items = root.querySelectorAll('.dakota-investment-details-item');
            for (const item of items) {
                const h3 = item.querySelector('h3');
                if ((h3?.textContent || '').trim() === arguments[0]) {
                    const desc = item.querySelector('.dakota-investment-description');
                    return desc ? (desc.textContent || '').trim() : '';
                }
            }
            return '';
            """,
            label,
        )
        assert text, f"Expected a displayed {label} value on the Investment Details tab."
        print(f"Investment Details {label}: {text}", flush=True)

    def verify_investment_details_tab_geography(self) -> None:
        with allure_step(self.driver, "Verify Investment Details tab is displayed"):
            self._wait_visible(self.INVESTMENT_DETAILS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investment Details tab"):
            self._open_investment_details_tab()
        with allure_step(self.driver, "Verify Investment Details tab displays Geography"):
            self._verify_investment_details_field(self.INVESTMENT_DETAILS_GEOGRAPHY_LABEL)

    def verify_investment_details_tab_industry(self) -> None:
        with allure_step(self.driver, "Verify Investment Details tab is displayed"):
            self._wait_visible(self.INVESTMENT_DETAILS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investment Details tab"):
            self._open_investment_details_tab()
        with allure_step(self.driver, "Verify Investment Details tab displays Industry"):
            self._verify_investment_details_field(self.INVESTMENT_DETAILS_INDUSTRY_LABEL)

    def verify_investment_details_tab_check_size(self) -> None:
        with allure_step(self.driver, "Verify Investment Details tab is displayed"):
            self._wait_visible(self.INVESTMENT_DETAILS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Investment Details tab"):
            self._open_investment_details_tab()
        with allure_step(self.driver, "Verify Investment Details tab displays Check Size"):
            self._verify_investment_details_field(self.INVESTMENT_DETAILS_CHECK_SIZE_LABEL)

    # ------------------------------------------------------------------
    # Platform details tab
    # ------------------------------------------------------------------

    def _open_platform_details_tab(self) -> None:
        self._wait_visible(self.PLATFORM_DETAILS_TAB_SELECTOR)
        self._click_shadow('a.dakota-tab-button[href*="/platform-details"]')
        time.sleep(1.5)
        print(f"Navigated to {self.PLATFORM_DETAILS_TAB_NAME} tab.", flush=True)

    def verify_company_platform_details_tab(self) -> None:
        with allure_step(self.driver, "Verify Platform Details tab is displayed"):
            self._wait_visible(self.PLATFORM_DETAILS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Platform Details tab"):
            self._open_platform_details_tab()

    def verify_platform_details_tab_platform_description(self) -> None:
        with allure_step(self.driver, "Verify Platform Details tab is displayed"):
            self._wait_visible(self.PLATFORM_DETAILS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Platform Details tab"):
            self._open_platform_details_tab()
        with allure_step(self.driver, "Verify Platform Details tab displays Platform Description"):
            text = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return '';
                const items = root.querySelectorAll('.dakota-platform-info-item');
                for (const item of items) {
                    const h3 = item.querySelector('h3');
                    if ((h3?.textContent || '').trim() === arguments[0]) {
                        const desc = item.querySelector('.dakota-platform-description');
                        return desc ? (desc.textContent || '').trim() : '';
                    }
                }
                return '';
                """,
                self.PLATFORM_DETAILS_PLATFORM_DESCRIPTION_LABEL,
            )
            assert text, (
                "Expected a displayed Platform Description value on the Platform Details tab."
            )
            print(
                f"Platform Details {self.PLATFORM_DETAILS_PLATFORM_DESCRIPTION_LABEL}: {text}",
                flush=True,
            )

    # ------------------------------------------------------------------
    # Contacts tab
    # ------------------------------------------------------------------

    def _open_contacts_tab(self) -> None:
        self.click_tab_by_name(self.CONTACTS_TAB_NAME)
        self.wait_for_contacts_loaded()
        print(f"Navigated to {self.CONTACTS_TAB_NAME} tab.", flush=True)

    def verify_contacts_tab_results(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Verify Contacts tab displays contacts or empty state"):
            self._verify_contacts_tab_content_displayed()

    def _verify_contacts_tab_content_displayed(self) -> None:
        def _ready(_driver):
            if self._query_count(self.CONTACT_ITEM_SELECTOR) > 0:
                return True
            texts = self._query_all_texts(".dakota-no-results p")
            return any(self.CONTACTS_NO_RESULTS_TEXT.lower() in t.lower() for t in texts)

        WebDriverWait(self.driver, self.timeout).until(_ready)
        if self._query_count(self.CONTACT_ITEM_SELECTOR) == 0:
            print(
                f"Contacts tab displayed empty state: {self.CONTACTS_NO_RESULTS_TEXT}",
                flush=True,
            )
        else:
            count = self._query_count(self.CONTACT_ITEM_SELECTOR)
            print(f"Contacts tab displayed {count} contact result(s).", flush=True)

    def verify_contacts_tab_contact_roles(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Verify all contacts on the page display a role"):
            self._verify_contacts_tab_roles_displayed()

    def _verify_contacts_tab_roles_displayed(self) -> None:
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) >= 1
        )
        roles = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return [];
            return Array.from(root.querySelectorAll('.contacts-dakota-record-item')).map(item => {
                const role = item.querySelector('.contacts-dakota-record-subDetails');
                return role ? (role.textContent || '').trim() : '';
            });
            """
        )
        for index, role_text in enumerate(roles, start=1):
            assert role_text, f"Contact {index} of {len(roles)} is missing a role."
            print(f"Contact {index} role: {role_text}", flush=True)
        print(f"All {len(roles)} contact(s) display a role.", flush=True)

    def verify_contacts_tab_contact_urls(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Verify all contacts on the page display a URL"):
            self._verify_contacts_tab_urls_displayed()

    def _verify_contacts_tab_urls_displayed(self) -> None:
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) >= 1
        )
        hrefs = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return [];
            return Array.from(root.querySelectorAll('.contacts-dakota-record-item')).map(item => {
                const link = item.querySelector('a.contacts-dakota-contact-link');
                return link ? (link.getAttribute('href') || '').trim() : '';
            });
            """
        )
        for index, href in enumerate(hrefs, start=1):
            assert href, f"Contact {index} of {len(hrefs)} is missing a URL href."
            print(f"Contact {index} URL: {href}", flush=True)
        print(f"All {len(hrefs)} contact(s) display a URL.", flush=True)

    def verify_contacts_tab_contact_emails(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Verify all contacts on the page display an email address"):
            self._verify_contacts_tab_emails_displayed()

    def _verify_contacts_tab_emails_displayed(self) -> None:
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) >= 1
        )
        emails = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return [];
            return Array.from(root.querySelectorAll('.contacts-dakota-record-item')).map(item => {
                const link = item.querySelector('.contacts-dakota-contact-email a.contacts-dakota-contact-link');
                return {
                    href: link ? (link.getAttribute('href') || '').trim() : '',
                    text: link ? (link.textContent || '').trim() : '',
                };
            });
            """
        )
        for index, email in enumerate(emails, start=1):
            assert email["href"].lower().startswith("mailto:"), (
                f"Contact {index} is missing a mailto email href."
            )
            assert email["text"], f"Contact {index} is missing email text."
            print(f"Contact {index} email: {email['text']}", flush=True)
        print(f"All {len(emails)} contact(s) display an email address.", flush=True)

    def verify_contacts_tab_search_results(self, contact_search_term: str) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(
            self.driver,
            f"Search contacts for '{contact_search_term}' and verify results",
        ):
            self._search_contacts_and_verify_results(contact_search_term)

    def _search_contacts_and_verify_results(self, contact_search_term: str) -> None:
        self._wait_visible("#contact-search")
        self._fill_shadow_input("#contact-search", contact_search_term)
        time.sleep(SEARCH_DEBOUNCE_SEC)
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) >= 1
            or any(
                self.CONTACTS_NO_RESULTS_TEXT.lower() in t.lower()
                for t in self._query_all_texts(".contacts-dakota-no-results p")
            )
        )
        self._verify_contacts_search_results_displayed(contact_search_term)

    def _verify_contacts_search_results_displayed(self, contact_search_term: str) -> None:
        no_results = any(
            self.CONTACTS_NO_RESULTS_TEXT.lower() in t.lower()
            for t in self._query_all_texts(".contacts-dakota-no-results p")
        )
        if no_results:
            pytest.fail(f"Contacts search for '{contact_search_term}' returned no results.")
        count = self._query_count(self.CONTACT_ITEM_SELECTOR)
        assert count >= 1, (
            f"Expected contacts search for '{contact_search_term}' to return results."
        )
        names = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return [];
            return Array.from(root.querySelectorAll('.contacts-dakota-record-name'))
                .map(el => (el.textContent || '').trim());
            """
        )
        search_lower = contact_search_term.lower()
        for index, name in enumerate(names, start=1):
            assert search_lower in name.lower(), (
                f"Contact {index} name '{name}' does not match search term '{contact_search_term}'."
            )
            print(f"Contact {index}: {name}", flush=True)
        print(
            f"Contacts search for '{contact_search_term}' returned {count} result(s).",
            flush=True,
        )

    def _open_first_contact_details(self) -> str:
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) >= 1
        )
        name = self._query_text(self.CONTACT_NAME_SELECTOR)
        assert name, "Expected the first contact to have a name before opening details."
        self._click_shadow(self.CONTACT_ITEM_SELECTOR)
        print(f"Clicked first contact: {name}", flush=True)
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._is_visible_in_shadow(self.CONTACT_DETAIL_PAGE_SELECTOR)
        )
        return name

    def verify_contacts_tab_contact_details(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Click the first contact and verify details are displayed"):
            contact_name = self._open_first_contact_details()
            self._verify_contact_details_displayed(contact_name)

    def _verify_contact_details_displayed(self, expected_contact_name: str) -> None:
        self._wait_visible(self.CONTACT_DETAIL_PAGE_SELECTOR)
        detail_name = self._query_text(self.CONTACT_DETAIL_NAME_SELECTOR)
        assert detail_name, "Contact detail page name is empty."
        assert detail_name.lower() == expected_contact_name.lower(), (
            f"Contact detail name '{detail_name}' does not match '{expected_contact_name}'."
        )
        fields = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return [];
            return Array.from(root.querySelectorAll('.contacts-dakota-detail-field')).map(field => {
                const label = field.querySelector('.contacts-dakota-detail-field-label');
                const value = field.querySelector('.contacts-dakota-detail-field-value');
                return {
                    label: label ? (label.textContent || '').trim() : '',
                    value: value ? (value.textContent || '').trim() : '',
                };
            });
            """
        )
        title_text = self._query_text(self.CONTACT_DETAIL_TITLE_SELECTOR)
        populated = sum(1 for f in fields if f.get("label") and f.get("value"))
        for field in fields:
            if field.get("label") and field.get("value"):
                print(f"Contact detail field: {field['label']} = {field['value']}", flush=True)
        assert title_text or populated >= 1, (
            f"Contact detail page for '{detail_name}' has no loaded data."
        )
        if title_text:
            print(f"Contact detail title: {title_text}", flush=True)

    def _verify_contact_detail_field(self, field_label: str) -> str:
        self._wait_visible(self.CONTACT_DETAIL_PAGE_SELECTOR)
        self._ensure_contact_detail_field_visible(field_label)
        value = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return '';
            const fields = root.querySelectorAll('.contacts-dakota-detail-field');
            for (const field of fields) {
                const label = field.querySelector('.contacts-dakota-detail-field-label');
                if ((label?.textContent || '').trim() === arguments[0]) {
                    const val = field.querySelector('.contacts-dakota-detail-field-value');
                    return val ? (val.textContent || '').trim() : '';
                }
            }
            return '';
            """,
            field_label,
        )
        assert value, f"{field_label} is displayed but has no value."
        print(f"{field_label}: {value}", flush=True)
        return str(value)

    def _ensure_contact_detail_field_visible(self, field_label: str) -> None:
        self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return;
            const fields = root.querySelectorAll('.contacts-dakota-detail-field');
            for (const field of fields) {
                const label = field.querySelector('.contacts-dakota-detail-field-label');
                if ((label?.textContent || '').trim() === arguments[0]) {
                    field.scrollIntoView({ block: 'center', inline: 'nearest' });
                    return;
                }
            }
            """,
            field_label,
        )

    def verify_contacts_tab_contact_type(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Click the first contact and verify Contact Type is displayed"):
            self._open_first_contact_details()
            self._verify_contact_detail_field(self.CONTACT_DETAIL_CONTACT_TYPE_LABEL)

    def verify_contacts_tab_contact_metro_area(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Click the first contact and verify Metro Area is displayed"):
            self._open_first_contact_details()
            self._verify_contact_detail_field(self.CONTACT_DETAIL_METRO_AREA_LABEL)

    def verify_contacts_tab_contact_phone(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Click the first contact and verify Phone is displayed"):
            self._open_first_contact_details()
            self._verify_contact_detail_field(self.CONTACT_DETAIL_PHONE_LABEL)
            phone_href = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return '';
                const fields = root.querySelectorAll('.contacts-dakota-detail-field');
                for (const field of fields) {
                    const label = field.querySelector('.contacts-dakota-detail-field-label');
                    if ((label?.textContent || '').trim() === arguments[0]) {
                        const link = field.querySelector('a.contacts-dakota-detail-field-link[href^="tel:"]');
                        return link ? (link.getAttribute('href') || '').trim() : '';
                    }
                }
                return '';
                """,
                self.CONTACT_DETAIL_PHONE_LABEL,
            )
            assert phone_href.lower().startswith("tel:"), (
                f"{self.CONTACT_DETAIL_PHONE_LABEL} link is missing a tel: href."
            )

    def verify_contacts_tab_contact_detail_email(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Click the first contact and verify Email is displayed"):
            self._open_first_contact_details()
            self._verify_contact_detail_field(self.CONTACT_DETAIL_EMAIL_LABEL)
            email_href = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return '';
                const fields = root.querySelectorAll('.contacts-dakota-detail-field');
                for (const field of fields) {
                    const label = field.querySelector('.contacts-dakota-detail-field-label');
                    if ((label?.textContent || '').trim() === arguments[0]) {
                        const link = field.querySelector('a.contacts-dakota-detail-field-link[href^="mailto:"]');
                        return link ? (link.getAttribute('href') || '').trim() : '';
                    }
                }
                return '';
                """,
                self.CONTACT_DETAIL_EMAIL_LABEL,
            )
            assert email_href.lower().startswith("mailto:"), (
                f"{self.CONTACT_DETAIL_EMAIL_LABEL} link is missing a mailto: href."
            )

    def verify_contacts_tab_contact_detail_linkedin_url(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(
            self.driver,
            "Click the first contact, scroll to LinkedIn URL if needed, and verify it is displayed",
        ):
            self._open_first_contact_details()
            self._verify_contact_detail_field(self.CONTACT_DETAIL_LINKEDIN_URL_LABEL)
            linkedin_href = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return '';
                const fields = root.querySelectorAll('.contacts-dakota-detail-field');
                for (const field of fields) {
                    const label = field.querySelector('.contacts-dakota-detail-field-label');
                    if ((label?.textContent || '').trim() === arguments[0]) {
                        const link = field.querySelector('a.contacts-dakota-detail-field-link');
                        return link ? (link.getAttribute('href') || '').trim() : '';
                    }
                }
                return '';
                """,
                self.CONTACT_DETAIL_LINKEDIN_URL_LABEL,
            )
            assert "linkedin.com" in linkedin_href.lower(), (
                f"{self.CONTACT_DETAIL_LINKEDIN_URL_LABEL} link is missing a LinkedIn href."
            )
            print(f"{self.CONTACT_DETAIL_LINKEDIN_URL_LABEL}: {linkedin_href}", flush=True)

    def verify_contacts_tab_go_back_to_contact_list(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Open the first contact details page"):
            self._open_first_contact_details()
        with allure_step(
            self.driver,
            f'Click "{self.CONTACT_DETAIL_BACK_BUTTON_TEXT}" and verify contacts list',
        ):
            self._go_back_to_contacts_list()
            self._verify_contacts_list_displayed()

    def _go_back_to_contacts_list(self) -> None:
        self._wait_visible(self.CONTACT_DETAIL_PAGE_SELECTOR)
        clicked = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            if (!root) return false;
            const buttons = root.querySelectorAll('.contacts-dakota-detail-back-button');
            for (const btn of buttons) {
                if (/go back to contact list/i.test(btn.textContent || '')) {
                    btn.click();
                    return true;
                }
            }
            return false;
            """
        )
        if not clicked:
            pytest.fail(f'Could not click "{self.CONTACT_DETAIL_BACK_BUTTON_TEXT}".')
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: not self._is_visible_in_shadow(self.CONTACT_DETAIL_PAGE_SELECTOR)
        )

    def _verify_contacts_list_displayed(self) -> None:
        self._wait_visible("#contact-search")
        header = self._query_text(self.CONTACTS_HEADER_SELECTOR)
        assert self.CONTACTS_TAB_NAME in header, "Contacts list header not displayed."
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) >= 1
        )
        count = self._query_count(self.CONTACT_ITEM_SELECTOR)
        print(f"Contacts list displayed {count} contact(s).", flush=True)

    def verify_contacts_tab_contact_count(self) -> None:
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Verify Contacts tab shows number of results displayed"):
            self._verify_contacts_tab_count_displayed()

    def _verify_contacts_tab_count_displayed(self) -> None:
        header_text = self._query_text(self.CONTACTS_HEADER_SELECTOR)
        match = re.search(r"Showing (\d+)", header_text, re.I)
        assert match, f"Could not parse contact count from '{header_text}'."
        displayed_count = int(match.group(1))
        print(f"Contacts tab count label: {header_text}", flush=True)
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) >= displayed_count
        )
        assert self._query_count(self.CONTACT_ITEM_SELECTOR) == displayed_count, (
            "Contacts tab count label does not match displayed contact results."
        )

    def scroll_contacts_tab_to_end(self) -> None:
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) >= 1
        )
        count = self._query_count(self.CONTACT_ITEM_SELECTOR)
        scroll_before = self._read_scroll_metrics(self.CONTACTS_SCROLL_CONTAINER_SELECTORS)
        if count > 1:
            self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                const items = root?.querySelectorAll('.contacts-dakota-record-item') || [];
                if (items.length) items[items.length - 1].scrollIntoView({ block: 'end' });
                """
            )
        self._scroll_shadow_container_to_end(self.CONTACTS_SCROLL_CONTAINER_SELECTORS)
        scroll_after = self._read_scroll_metrics(self.CONTACTS_SCROLL_CONTAINER_SELECTORS)
        print(
            f"Contacts tab scroll: before={scroll_before}, after={scroll_after}",
            flush=True,
        )

    def _contacts_load_more_visible(self) -> bool:
        return bool(
            self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return false;
                const btn = root.querySelector('button.contacts-dakota-load-more-button');
                return !!(btn && btn.offsetParent !== null);
                """
            )
        )

    def _ensure_load_more_contacts_button_visible(self) -> None:
        for _ in range(60):
            if self._contacts_load_more_visible():
                return
            self._scroll_shadow_container_to_end(self.CONTACTS_SCROLL_CONTAINER_SELECTORS)
            time.sleep(0.2)
        if not self._contacts_load_more_visible():
            pytest.fail(
                f"{self.LOAD_MORE_CONTACTS_BUTTON_TEXT} button is not visible "
                "in the Contacts tab viewport after scrolling."
            )

    def _verify_contacts_tab_load_more_visibility(self, total_contacts: int) -> None:
        if total_contacts > self.CONTACTS_PAGE_SIZE:
            self._ensure_load_more_contacts_button_visible()
            print(
                f"{self.LOAD_MORE_CONTACTS_BUTTON_TEXT} button is visible for "
                f"{total_contacts} contacts.",
                flush=True,
            )
            return
        assert not self._contacts_load_more_visible(), (
            f"{self.LOAD_MORE_CONTACTS_BUTTON_TEXT} button should not be displayed "
            f"when the General tab shows {total_contacts} contacts."
        )
        print(
            f"{self.LOAD_MORE_CONTACTS_BUTTON_TEXT} button is not displayed for "
            f"{total_contacts} contacts.",
            flush=True,
        )

    def _load_more_contacts(self) -> None:
        count_before = self._query_count(self.CONTACT_ITEM_SELECTOR)
        assert count_before >= 1, (
            f"Expected contacts before {self.LOAD_MORE_CONTACTS_BUTTON_TEXT}."
        )
        clicked = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            const btn = root?.querySelector('button.contacts-dakota-load-more-button');
            if (btn) { btn.click(); return true; }
            const buttons = root?.querySelectorAll('button') || [];
            for (const b of buttons) {
                if (/load more/i.test((b.textContent || '').trim())) {
                    b.click();
                    return true;
                }
            }
            return false;
            """
        )
        if not clicked:
            pytest.fail(f"{self.LOAD_MORE_CONTACTS_BUTTON_TEXT} button not found.")
        WebDriverWait(self.driver, self.timeout).until(
            lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) > count_before
        )

    def verify_contacts_tab_load_more_button(self) -> None:
        with allure_step(self.driver, "Read Contacts count on General tab"):
            general_value = self._get_general_tab_stat_value(self.CONTACTS_TAB_NAME)
            general_count = self._parse_contacts_stat_count(general_value)
            print(f"General tab Contacts count: {general_value} ({general_count})", flush=True)
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Scroll Contacts tab to the end of the list"):
            self.scroll_contacts_tab_to_end()
        with allure_step(
            self.driver,
            "Verify Load more button visibility matches General tab contact count",
        ):
            self._verify_contacts_tab_load_more_visibility(general_count)

    def verify_contacts_tab_load_more_displays_more(self) -> None:
        with allure_step(self.driver, "Read Contacts count on General tab"):
            general_value = self._get_general_tab_stat_value(self.CONTACTS_TAB_NAME)
            general_count = self._parse_contacts_stat_count(general_value)
            print(f"General tab Contacts count: {general_value} ({general_count})", flush=True)
            assert general_count > self.CONTACTS_PAGE_SIZE, (
                f"Expected more than {self.CONTACTS_PAGE_SIZE} contacts to verify "
                f"Load more displays more, but General tab shows {general_count}."
            )
        with allure_step(self.driver, "Verify Contacts tab is displayed"):
            self._wait_visible(self.CONTACTS_TAB_SELECTOR)
        with allure_step(self.driver, "Navigate to Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Scroll Contacts tab until Load more is visible"):
            self.scroll_contacts_tab_to_end()
            self._ensure_load_more_contacts_button_visible()
        with allure_step(self.driver, 'Click "Load more" to fetch additional contacts'):
            self._load_more_contacts()
        with allure_step(self.driver, "Scroll Contacts tab to the end of the list"):
            self.scroll_contacts_tab_to_end()

    def verify_contacts_count_matches_general_tab(self) -> None:
        with allure_step(self.driver, "Read Contacts count on General tab"):
            general_value = self._get_general_tab_stat_value(self.CONTACTS_TAB_NAME)
            general_count = self._parse_contacts_stat_count(general_value)
            print(f"General tab Contacts count: {general_value} ({general_count})", flush=True)
        with allure_step(self.driver, "Open Contacts tab"):
            self._open_contacts_tab()
        with allure_step(self.driver, "Verify Contacts tab count matches General tab"):
            contacts_count = self._count_contacts_on_contacts_tab()
            print(f"Contacts tab displayed count: {contacts_count}", flush=True)
            assert contacts_count == general_count, (
                "Contacts tab count does not match General tab Contacts stat. "
                f"General tab: {general_count}, Contacts tab: {contacts_count}"
            )

    def _count_contacts_on_contacts_tab(self) -> int:
        try:
            WebDriverWait(self.driver, self.timeout).until(
                lambda d: self._query_count(self.CONTACT_ITEM_SELECTOR) >= 1
            )
        except TimeoutException:
            return 0
        return self._query_count(self.CONTACT_ITEM_SELECTOR)

    # ------------------------------------------------------------------
    # Public verify_dakota_* entry points (login handled by conftest)
    # ------------------------------------------------------------------

    def verify_dakota_search_results(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)

    def verify_external_page_auto_search_results(self, page_url: str) -> None:
        attempts = 3 if self._is_linkedin_url(page_url) else 1
        last_error = None
        for attempt in range(1, attempts + 1):
            try:
                self.open_external_page_and_sidebar(page_url)
                self.ensure_sidebar_ready()
                self.verify_sidebar_prefilled_search_and_results(page_url)
                return
            except Exception as exc:  # pragma: no cover - defensive retry path
                last_error = exc
                if attempt == attempts:
                    raise
                # LinkedIn can intermittently redirect to authwall; recover and retry.
                self._clear_linkedin_cookies()
                self.driver.get("https://www.linkedin.com")
                time.sleep(1)
        if last_error is not None:
            raise last_error

    def verify_dakota_search_results_scroll(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.scroll_search_results_to_end(search_term)

    def verify_dakota_search_results_load_more(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.scroll_search_results_to_end(search_term)
        self.load_more_search_results(search_term)

    def verify_dakota_company_details(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_search_result_and_verify_company_details(search_term)

    def verify_dakota_company_general_tab(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_stat_cards()

    def verify_dakota_contacts_count_matches_general_tab(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_count_matches_general_tab()

    def verify_dakota_company_account_overview(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_account_overview()

    def verify_dakota_company_general_tab_type(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_type()

    def verify_dakota_company_general_tab_metro_area(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_metro_area()

    def verify_dakota_company_general_tab_website(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_website()

    def verify_dakota_company_general_tab_linkedin_url(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_linkedin_url()

    def verify_dakota_company_general_tab_billing_address(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_billing_address()

    def verify_dakota_company_investors_tab(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_company_investors_tab()

    def verify_dakota_company_investment_details_tab(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_search_result_for_tab(self.INVESTMENT_DETAILS_TAB_NAME)
        self.verify_company_investment_details_tab()

    def verify_dakota_company_platform_details_tab(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_allocator_search_result()
        self.verify_company_platform_details_tab()

    def verify_dakota_platform_details_tab_platform_description(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_allocator_search_result()
        self.verify_platform_details_tab_platform_description()

    def verify_dakota_contacts_tab_results(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_results()

    def verify_dakota_contacts_tab_contact_count(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_count()

    def verify_dakota_contacts_tab_load_more_button(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_load_more_button()

    def verify_dakota_contacts_tab_load_more_displays_more(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_load_more_displays_more()

    def verify_dakota_contacts_tab_contact_roles(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_roles()

    def verify_dakota_contacts_tab_contact_urls(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_urls()

    def verify_dakota_contacts_tab_contact_emails(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_emails()

    def verify_dakota_contacts_tab_search_results(
        self,
        company_search_term: str,
        contact_search_term: str,
    ) -> None:
        self.search_and_verify_results(company_search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_search_results(contact_search_term)

    def verify_dakota_contacts_tab_contact_details(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_details()

    def verify_dakota_contacts_tab_contact_type(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_type()

    def verify_dakota_contacts_tab_contact_metro_area(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_metro_area()

    def verify_dakota_contacts_tab_contact_phone(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_phone()

    def verify_dakota_contacts_tab_contact_detail_email(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_detail_email()

    def verify_dakota_contacts_tab_contact_detail_linkedin_url(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_detail_linkedin_url()

    def verify_dakota_contacts_tab_go_back_to_contact_list(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_go_back_to_contact_list()

    def verify_dakota_investors_tab_results(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_results()

    def verify_dakota_investment_details_tab_details(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_search_result_for_tab(self.INVESTMENT_DETAILS_TAB_NAME)
        self.verify_investment_details_tab_details()

    def verify_dakota_investment_details_tab_geography(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_search_result_for_tab(self.INVESTMENT_DETAILS_TAB_NAME)
        self.verify_investment_details_tab_geography()

    def verify_dakota_investment_details_tab_industry(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_search_result_for_tab(self.INVESTMENT_DETAILS_TAB_NAME)
        self.verify_investment_details_tab_industry()

    def verify_dakota_investment_details_tab_check_size(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_search_result_for_tab(self.INVESTMENT_DETAILS_TAB_NAME)
        self.verify_investment_details_tab_check_size()

    def verify_dakota_investors_tab_investor_count(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_investor_count()

    def verify_dakota_investors_tab_load_more_button(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_load_more_button()

    def verify_dakota_investors_tab_load_more_displays_more(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_load_more_displays_more()

    def verify_dakota_investors_tab_investor_metro_areas(self, search_term: str) -> None:
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_investor_metro_areas()
