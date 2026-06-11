import random

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class GoogleHomePage(BasePage):
    ACCEPT_ALL_BUTTON = "button:has-text('Accept all')"
    REJECT_ALL_BUTTON = "button:has-text('Reject all')"

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def handle_consent_if_present(self) -> None:
        if self.page.locator(self.ACCEPT_ALL_BUTTON).is_visible(timeout=2000):
            self.page.locator(self.ACCEPT_ALL_BUTTON).click()
        elif self.page.locator(self.REJECT_ALL_BUTTON).is_visible(timeout=2000):
            self.page.locator(self.REJECT_ALL_BUTTON).click()

    def open_chrome_web_store_in_new_tab(self, web_store_url: str) -> None:
        # Browser chrome controls (3-dot menu -> Extensions) are outside DOM automation scope.
        self.page.evaluate("(url) => window.open(url, '_blank')", web_store_url)

    def open_chrome_web_store_tab(self, base_url: str, web_store_url: str) -> Page:
        """Open Google, handle consent, and return the new Chrome Web Store tab."""
        with allure.step("Open Google homepage"):
            self.open(base_url)
            self.handle_consent_if_present()

        with allure.step("Open Chrome Web Store in a new tab"):
            with self.page.context.expect_page() as new_tab_info:
                self.open_chrome_web_store_in_new_tab(web_store_url)
            web_store_tab = new_tab_info.value
            web_store_tab.wait_for_load_state("domcontentloaded")
            return web_store_tab

    def search_for(self, term: str) -> None:
        """Search for a term by typing into the search bar to mimic human behavior."""
        # Find the search input
        search_input = self.page.locator("textarea[name='q'], input[name='q']").first
        search_input.wait_for(state="visible", timeout=5000)
        
        # Mimic human: Random mouse movement (jitter) near the search bar
        box = search_input.bounding_box()
        if box:
            for _ in range(3):
                self.page.mouse.move(
                    box['x'] + box['width'] / 2 + random.randint(-20, 20),
                    box['y'] + box['height'] / 2 + random.randint(-10, 10)
                )
                self.page.wait_for_timeout(random.randint(50, 150))

        # Mimic human: Hover then wait a bit before clicking
        search_input.hover()
        self.page.wait_for_timeout(random.randint(400, 1000))
        search_input.click()
        
        # Mimic human: Type with randomized delays between characters
        # Using locator.type with delay is more efficient than a manual loop
        search_input.type(term, delay=random.randint(100, 250))
            
        self.page.wait_for_timeout(random.randint(500, 1200))
        
        # Occasionally click the search button instead of pressing Enter
        if random.random() > 0.5:
            # Common search button selectors
            search_button = self.page.locator("input[name='btnK'], button[type='submit']").last
            try:
                if search_button.is_visible(timeout=2000):
                    # Use a short timeout for the click to avoid long hangs if intercepted
                    search_button.click(timeout=3000)
                else:
                    search_input.press("Enter")
            except Exception:
                # If click is intercepted or fails, fall back to Enter
                search_input.press("Enter")
        else:
            search_input.press("Enter")

            
        # Use domcontentloaded instead of networkidle to avoid timeouts from background requests
        self.page.wait_for_load_state("domcontentloaded")

