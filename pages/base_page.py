import allure
from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page) -> None:
        self.page = page

    def goto(self, url: str) -> None:
        with allure.step(f"Navigate to: {url}"):
            self.page.goto(url, wait_until="domcontentloaded")

    def open(self, url: str) -> None:
        self.goto(url)

    def get_title(self) -> str:
        with allure.step("Read page title"):
            return self.page.title()

    def get_current_url(self) -> str:
        with allure.step("Read current URL"):
            return self.page.url

    def click(self, selector: str) -> None:
        with allure.step(f"Click element: {selector}"):
            self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        with allure.step(f"Fill element: {selector}"):
            self.page.locator(selector).fill(value)

    def get_text(self, selector: str) -> str:
        with allure.step(f"Read text from: {selector}"):
            return self.page.locator(selector).inner_text()

    def is_visible(self, selector: str) -> bool:
        with allure.step(f"Check visibility of: {selector}"):
            return self.page.locator(selector).is_visible()
