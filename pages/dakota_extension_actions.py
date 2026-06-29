"""
Shared Dakota extension search/navigation helpers.

Core wait patterns from Dakota_Ext_Performance/pages/dakota_performance.py
(without performance benchmarking / Excel reporting).
"""

import time
from dataclasses import dataclass

import pytest
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from pages.dakota_auth import open_dakota_sidebar

DEFAULT_TIMEOUT = 60
SEARCH_DEBOUNCE_SEC = 1.5
VISIBILITY_PAUSE_SEC = 3


@dataclass
class SearchTiming:
    elapsed_s: float
    result_count: int
    has_load_more: bool


class DakotaExtensionActions:
    """Company search and navigation via Selenium + Shadow DOM."""

    def __init__(self, driver: webdriver.Chrome) -> None:
        self.driver = driver

    def _js(self, script: str, *args):
        return self.driver.execute_script(script, *args)

    def _shadow_ready(self) -> bool:
        return bool(
            self._js("return !!(document.getElementById('crxjs-app')?.shadowRoot);")
        )

    def _wait_shadow(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        WebDriverWait(self.driver, timeout).until(lambda d: self._shadow_ready())

    def clear_search(self) -> None:
        self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            const close = root?.querySelector('.dakota-search-close-button');
            if (close) { close.click(); return; }
            const input = root?.querySelector('#company-search');
            if (input) {
                input.value = '';
                input.dispatchEvent(new Event('input', { bubbles: true }));
            }
            """
        )
        time.sleep(SEARCH_DEBOUNCE_SEC)

    def type_search_term(self, term: str) -> None:
        open_dakota_sidebar(self.driver)
        self.clear_search()
        self._js(
            """
            const input = document.getElementById('crxjs-app')?.shadowRoot
                ?.querySelector('#company-search');
            if (!input) return false;
            input.focus();
            input.value = arguments[0];
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            return true;
            """,
            term,
        )
        time.sleep(SEARCH_DEBOUNCE_SEC)

    def wait_for_search_finished(self, timeout: int = DEFAULT_TIMEOUT) -> SearchTiming:
        start = time.perf_counter()

        def _done(_driver):
            return self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return null;
                const loading = root.querySelector('.dakota-loading');
                if (loading && loading.offsetParent !== null) return null;
                const rows = root.querySelectorAll('.dakota-record-item');
                const noResults = root.querySelector('.dakota-no-results');
                const error = root.querySelector('.dakota-error');
                if (rows.length || (noResults && noResults.offsetParent !== null)
                    || (error && error.offsetParent !== null)) {
                    return {
                        count: rows.length,
                        hasLoadMore: !!root.querySelector('.dakota-load-more-button'),
                    };
                }
                return null;
                """
            )

        try:
            state = WebDriverWait(self.driver, timeout).until(_done)
        except TimeoutException as exc:
            raise TimeoutException("Timed out waiting for search results.") from exc

        return SearchTiming(
            elapsed_s=time.perf_counter() - start,
            result_count=int(state["count"]),
            has_load_more=bool(state["hasLoadMore"]),
        )

    def search_company(self, term: str) -> SearchTiming:
        self.type_search_term(term)
        return self.wait_for_search_finished()

    def get_first_result_info(self) -> tuple[str, str]:
        info = self._js(
            """
            const row = document.getElementById('crxjs-app')?.shadowRoot
                ?.querySelector('.dakota-record-item');
            if (!row) return null;
            const name = row.querySelector('.dakota-record-name, .dakota-record-title');
            const ctype = row.querySelector('.dakota-record-type');
            return {
                name: (name?.textContent || '').trim(),
                type: (ctype?.textContent || '').trim(),
            };
            """
        )
        if not info:
            pytest.fail("No search result row found to open.")
        return info["name"], info["type"]

    def click_first_search_result(self) -> tuple[str, str]:
        name, ctype = self.get_first_result_info()
        self._js(
            """
            const row = document.getElementById('crxjs-app')?.shadowRoot
                ?.querySelector('.dakota-record-item');
            if (row) row.click();
            """
        )
        return name, ctype

    def wait_for_company_detail(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda d: self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                const header = root?.querySelector('.dakota-company-header');
                return !!(header && header.offsetParent !== null);
                """
            )
        )

    def click_tab_by_name(self, tab_name: str) -> None:
        clicked = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            const target = (arguments[0] || '').trim().toLowerCase();
            const links = root?.querySelectorAll(
                '.dakota-tab-button-container a, a.dakota-tab-button'
            ) || [];
            for (const link of links) {
                if ((link.textContent || '').trim().toLowerCase().includes(target)) {
                    link.scrollIntoView({ block: 'center' });
                    link.click();
                    return true;
                }
            }
            return false;
            """,
            tab_name,
        )
        if not clicked:
            pytest.fail(f"Tab '{tab_name}' not found in extension.")
        time.sleep(VISIBILITY_PAUSE_SEC)

    def wait_for_contacts_loaded(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda d: self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                const ready = root?.querySelector(
                    '.contacts-dakota-record-item, .contacts-dakota-no-results, '
                    + '.contacts-dakota-error, .dakota-contact-name'
                );
                const loading = root?.querySelector(
                    '.contacts-dakota-loading, .dakota-loading-contacts-text'
                );
                return !!(ready && ready.offsetParent !== null
                    && !(loading && loading.offsetParent !== null));
                """
            )
        )

    def wait_for_investors_tab_ready(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        """Investors tab may show items or an empty-state message."""

        def _ready(_driver):
            state = self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                if (!root) return null;
                const loading = root.querySelector('.dakota-loading');
                if (loading && loading.offsetParent !== null) return null;
                const items = root.querySelectorAll('.dakota-investor-item');
                const noResults = root.querySelector('.dakota-no-results p');
                if (items.length) return { count: items.length };
                if (noResults && noResults.offsetParent !== null
                    && /no investors found/i.test(noResults.textContent || '')) {
                    return { count: 0 };
                }
                return null;
                """
            )
            return state

        WebDriverWait(self.driver, timeout).until(_ready)

    def scroll_and_click_load_more(self, timeout: int = DEFAULT_TIMEOUT) -> None:
        revealed = self._js(
            """
            const root = document.getElementById('crxjs-app')?.shadowRoot;
            const body = root?.querySelector('.dakota-sidebar-body, .dakota-loggedin-body');
            const btn = root?.querySelector('.dakota-load-more-button');
            if (!btn || !body) return false;
            body.scrollTop = body.scrollHeight;
            btn.scrollIntoView({ block: 'center' });
            btn.click();
            return true;
            """
        )
        if not revealed:
            pytest.fail("Load More button not found.")

        WebDriverWait(self.driver, timeout).until(
            lambda d: self._js(
                """
                const root = document.getElementById('crxjs-app')?.shadowRoot;
                const loading = root?.querySelector('.dakota-loading-more-text');
                if (loading && loading.offsetParent !== null) return false;
                const rows = root?.querySelectorAll('.dakota-record-item') || [];
                return rows.length > 10;
                """
            )
        )
