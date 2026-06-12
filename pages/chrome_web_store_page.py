import re
import time

import allure
import pyautogui
from playwright.sync_api import Locator, Page, expect

from pages.base_page import BasePage
from utils.config import Config


class ChromeWebStorePage(BasePage):
    SEARCH_INPUT_CANDIDATES = (
        "input[aria-label='Search extensions and themes']",
        "input[type='search']",
        "input[placeholder*='Search']",
    )
    SEARCH_TRIGGER_BUTTON = "button[aria-label*='Search']"
    SWITCH_TO_CHROME_NO_THANKS_BUTTONS = (
        "button:has-text('No thanks')",
        "button:has-text('No Thanks')",
        "button:has-text('No, thanks')",
        "button:has-text('No, Thanks')",
    )
    RESULT_CANDIDATES = (
        "a[href*='/detail/']",
        "main a[href*='/detail/']",
        "div[role='list']",
        "main",
    )

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def _resolve_search_box(self) -> Locator:
        for selector in self.SEARCH_INPUT_CANDIDATES:
            candidate = self.page.locator(selector).first
            if candidate.is_visible(timeout=3000):
                return candidate

        trigger = self.page.locator(self.SEARCH_TRIGGER_BUTTON).first
        if trigger.is_visible(timeout=3000):
            trigger.click()
            for selector in self.SEARCH_INPUT_CANDIDATES:
                candidate = self.page.locator(selector).first
                if candidate.is_visible(timeout=3000):
                    return candidate

        raise AssertionError("Chrome Web Store search input was not found.")

    def dismiss_switch_to_chrome_dialog_if_present(self) -> None:
        for selector in self.SWITCH_TO_CHROME_NO_THANKS_BUTTONS:
            button = self.page.locator(selector).first
            if button.is_visible(timeout=2000):
                button.click()
                return

        role_based_button = self.page.get_by_role(
            "button", name=re.compile(r"no,?\s*thanks", re.I)
        )
        if role_based_button.first.is_visible(timeout=2000):
            role_based_button.first.click()

    def search_extension(self, keyword: str) -> None:
        self.page.wait_for_load_state("domcontentloaded")

        self.dismiss_switch_to_chrome_dialog_if_present()
        search_box = self._resolve_search_box()
        expect(search_box).to_be_visible()
        search_box.click()
        search_box.fill("")
        search_box.fill(keyword)

        search_box.press("Enter")
        self.page.wait_for_timeout(500)
        if "/search/" not in self.page.url:
            self.page.keyboard.press("Enter")
            self.page.wait_for_timeout(500)
        if "/search/" not in self.page.url:
            trigger = self.page.locator(self.SEARCH_TRIGGER_BUTTON).first
            if trigger.is_visible(timeout=2000):
                trigger.click()
                self.page.wait_for_timeout(500)

        if "/search/" not in self.page.url:
            self.page.goto(f"{Config.WEB_STORE_URL}search/{keyword}")

    def wait_for_results(self, keyword: str) -> None:
        expect(self.page).to_have_url(
            re.compile(rf".*/search/{re.escape(keyword)}.*"), timeout=15000
        )
        self.page.wait_for_load_state("domcontentloaded")

        for selector in self.RESULT_CANDIDATES:
            candidate = self.page.locator(selector).first
            if candidate.is_visible(timeout=5000):
                return

        if "/search/" in self.page.url:
            return

        raise AssertionError("Search results page was not displayed in Chrome Web Store.")

    def open_dakota_marketplace_result(self) -> None:
        result_link = self.page.get_by_role(
            "link", name=re.compile(r"Dakota Marketplace", re.I)
        ).first

        expect(result_link).to_be_visible(timeout=10000)
        result_link.click()

    def wait_for_dakota_marketplace_details_page(self) -> None:
        expect(self.page).to_have_url(re.compile(r".*/detail/.*", re.I), timeout=15000)
        expect(self.page).to_have_title(re.compile(r".*Dakota Marketplace.*", re.I))

    def click_add_to_chrome(self) -> bool:
        install_chrome_button = self.page.get_by_role(
            "button", name=re.compile(r"install chrome", re.I)
        ).first
        add_button = self.page.locator("button").filter(
            has_text=re.compile(r"add to (chrome|brave|edge)", re.I)
        ).first
        remove_button = self.page.locator("button").filter(
            has_text=re.compile(r"remove from (chrome|brave|edge)", re.I)
        ).first

        try:
            combined_button = self.page.locator("button").filter(
                has_text=re.compile(r"(add to|remove from) (chrome|brave|edge)", re.I)
            ).first
            combined_button.wait_for(state="visible", timeout=30000)

            if install_chrome_button.is_visible(timeout=1000):
                raise AssertionError(
                    "Chrome Web Store is asking you to switch to Chrome before "
                    "installing the extension. Launch the test with a Chrome "
                    "channel and a persistent profile."
                )

            for _ in range(15):
                if remove_button.is_visible(timeout=500):
                    return False

                if add_button.is_visible(timeout=500) and not add_button.is_disabled():
                    add_button.click()
                    return True

                self.page.wait_for_timeout(1000)

            if remove_button.is_visible(timeout=2000):
                return False

            if add_button.is_visible(timeout=1000) and add_button.is_disabled():
                print(
                    "Add to Chrome is disabled; treating extension as already installed."
                )
                return False
        except AssertionError:
            raise
        except Exception:
            return False

        return False

    def wait_for_remove_from_chrome(self) -> None:
        remove_button = self.page.get_by_role(
            "button", name=re.compile(r"remove\s*from\s*(chrome|brave|edge)", re.I)
        ).first

        if remove_button.is_visible(timeout=5000):
            return

        self.page.wait_for_timeout(3000)
        pyautogui.press("left")
        self.page.wait_for_timeout(500)
        pyautogui.press("enter")
        expect(remove_button).to_be_visible(timeout=45000)
        self.page.wait_for_timeout(2000)

    def _native_left_click(self, position: tuple[int, int]) -> None:
        x, y = position
        pyautogui.moveTo(x, y, duration=0.15)
        time.sleep(0.2)
        pyautogui.click(x=x, y=y, button="left")

    def dismiss_install_toast(self) -> None:
        # Chrome shows a temporary native "installed" bubble near the toolbar.
        # Dismiss it with Escape instead of another coordinate click.
        time.sleep(Config.INSTALL_TOAST_APPEAR_WAIT_SECONDS)
        pyautogui.press("esc")
        time.sleep(Config.INSTALL_TOAST_CLOSE_SETTLE_SECONDS)

    def pin_dakota_extension_in_toolbar(self) -> None:
        self.dismiss_install_toast()
        self._native_left_click(Config.EXTENSION_MENU_ICON_POSITION)
        time.sleep(5)
        self._native_left_click(Config.DAKOTA_PIN_ICON_POSITION)
        time.sleep(5)

    def assert_extension_already_installed(self) -> None:
        remove_button = self.page.locator("button").filter(
            has_text=re.compile(r"remove from (chrome|brave|edge)", re.I)
        ).first
        expect(remove_button).to_be_visible(timeout=10000)

    def install_dakota_marketplace_extension(self, search_term: str) -> None:
        with allure.step("Dismiss 'Switch to Chrome?' dialog if it appears"):
            self.dismiss_switch_to_chrome_dialog_if_present()

        with allure.step("Search for Dakota and wait for results"):
            self.search_extension(search_term)
            self.wait_for_results(search_term)

        with allure.step("Open Dakota Marketplace from search results"):
            self.open_dakota_marketplace_result()
            self.wait_for_dakota_marketplace_details_page()

        with allure.step("Click Add to Chrome"):
            is_newly_installed = self.click_add_to_chrome()

        if is_newly_installed:
            with allure.step(
                "Wait for extension to be added (Remove from Chrome button visible)"
            ):
                self.wait_for_remove_from_chrome()
            with allure.step("Pin the Dakota extension using pyautogui"):
                self.pin_dakota_extension_in_toolbar()
        else:
            with allure.step(
                "Confirm extension is already installed (Remove from Chrome visible)"
            ):
                self.assert_extension_already_installed()
            with allure.step("Ensure Dakota extension is pinned in the toolbar"):
                self.pin_dakota_extension_in_toolbar()
