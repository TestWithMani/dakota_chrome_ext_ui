"""Allure steps, screenshots, and failure attachments for Selenium tests."""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from selenium.webdriver.chrome.webdriver import WebDriver

try:
    import allure
except ImportError:
    allure = None

_PAGE_SOURCE_MAX_BYTES = 80_000


def allure_available() -> bool:
    return allure is not None


def attach_text(content: str, name: str) -> None:
    if not allure_available() or not content:
        return
    allure.attach(content, name=name, attachment_type=allure.attachment_type.TEXT)


def attach_screenshot(driver: "WebDriver", name: str = "Screenshot") -> None:
    if not allure_available():
        return
    try:
        png = driver.get_screenshot_as_png()
    except Exception:
        return
    if not png:
        return
    allure.attach(png, name=name, attachment_type=allure.attachment_type.PNG)


def attach_page_source(driver: "WebDriver", name: str = "Page HTML") -> None:
    if not allure_available():
        return
    try:
        html = driver.page_source or ""
    except Exception:
        return
    if len(html.encode("utf-8")) > _PAGE_SOURCE_MAX_BYTES:
        html = html[:_PAGE_SOURCE_MAX_BYTES] + "\n\n... [truncated]"
    attach_text(html, name)


def attach_browser_logs(driver: "WebDriver", name: str = "Browser console") -> None:
    if not allure_available():
        return
    try:
        entries = driver.get_log("browser")
    except Exception:
        return
    if not entries:
        return
    lines = []
    for entry in entries[-40:]:
        level = entry.get("level", "INFO")
        message = entry.get("message", "")
        lines.append(f"[{level}] {message}")
    attach_text("\n".join(lines), name)


@contextmanager
def allure_step(driver: "WebDriver | None", title: str, *, screenshot: bool = True):
    if not allure_available():
        yield
        return

    with allure.step(title):
        yield
        if screenshot and driver is not None:
            attach_screenshot(driver, title)


def attach_page_info(driver: "WebDriver", label: str = "Page info") -> None:
    if not allure_available():
        return
    try:
        handles = driver.window_handles
        info = (
            f"URL: {driver.current_url}\n"
            f"Title: {driver.title}\n"
            f"Window handles: {len(handles)}"
        )
    except Exception:
        return
    attach_text(info, label)


def attach_failure_bundle(
    driver: "WebDriver | None",
    *,
    test_name: str,
    failure_text: str,
    phase: str,
) -> None:
    """Attach screenshot, page context, HTML, and traceback for a failed test phase."""
    if not allure_available():
        return

    with allure.step(f"Capture failure evidence ({phase})"):
        attach_text(failure_text, f"Failure details — {test_name} ({phase})")
        if driver is None:
            attach_text("No WebDriver fixture was available for this test.", "Driver")
            return
        attach_screenshot(driver, f"Failure screenshot ({phase})")
        attach_page_info(driver, f"Failure page info ({phase})")
        attach_page_source(driver, f"Failure page HTML ({phase})")
        attach_browser_logs(driver, f"Browser console ({phase})")
