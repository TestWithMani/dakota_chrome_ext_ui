import re

from playwright.sync_api import Page, expect


def dismiss_marketplace_obstructions(page: Page) -> None:
    """Dismiss site overlays that block the extension sidebar from opening."""
    _dismiss_cookie_banner(page)
    _dismiss_sign_in_overlay(page)


def _dismiss_cookie_banner(page: Page) -> None:
    cookie_dialog = page.get_by_role("dialog", name=re.compile(r"cookie", re.I))
    accept_candidates = (
        cookie_dialog.get_by_role("button", name=re.compile(r"^Accept$", re.I)),
        page.locator("button").filter(has_text=re.compile(r"^Accept$", re.I)),
        page.get_by_role("button", name=re.compile(r"^Accept$", re.I)),
    )

    for accept in accept_candidates:
        try:
            button = accept.first
            if button.is_visible(timeout=2000):
                button.click(force=True)
                page.wait_for_timeout(1000)
                break
        except Exception:
            continue

    try:
        expect(cookie_dialog).to_be_hidden(timeout=5000)
    except Exception:
        pass


def _dismiss_sign_in_overlay(page: Page) -> None:
    close_sign_in = page.get_by_role("button", name=re.compile(r"close sign in", re.I))
    if close_sign_in.first.is_visible(timeout=2000):
        close_sign_in.first.evaluate("el => el.click()")
        page.wait_for_timeout(500)
