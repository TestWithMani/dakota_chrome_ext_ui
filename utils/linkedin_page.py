import re
from urllib.parse import parse_qs, unquote, urlparse

import pytest
from playwright.sync_api import BrowserContext, Page, expect

from utils.marketplace_page import dismiss_external_page_obstructions


def is_linkedin_url(url: str) -> bool:
    return "linkedin.com" in url.lower()


def is_linkedin_authwall(url: str) -> bool:
    return "linkedin.com/authwall" in url.lower()


def clear_linkedin_cookies(context: BrowserContext) -> None:
    """Drop LinkedIn session cookies so the browser is treated like a fresh guest."""
    cookies = context.cookies()
    non_linkedin = [
        cookie
        for cookie in cookies
        if "linkedin.com" not in cookie.get("domain", "").lower()
    ]
    context.clear_cookies()
    if non_linkedin:
        context.add_cookies(non_linkedin)


def extract_session_redirect(url: str) -> str | None:
    params = parse_qs(urlparse(url).query)
    redirects = params.get("sessionRedirect", [])
    if not redirects:
        return None
    return unquote(redirects[0])


def open_linkedin_public_page(page: Page, target_url: str) -> None:
    """Open a public LinkedIn page without being forced to the auth wall."""
    context = page.context
    normalized_target = target_url.rstrip("/")

    clear_linkedin_cookies(context)
    page.goto(
        target_url,
        wait_until="domcontentloaded",
        referer="https://www.google.com/",
    )
    page.wait_for_timeout(1500)
    dismiss_external_page_obstructions(page)

    if is_linkedin_authwall(page.url):
        redirect_target = extract_session_redirect(page.url) or target_url
        clear_linkedin_cookies(context)
        page.goto(
            redirect_target,
            wait_until="domcontentloaded",
            referer="https://www.google.com/",
        )
        page.wait_for_timeout(1500)
        dismiss_external_page_obstructions(page)

    if is_linkedin_authwall(page.url):
        pytest.fail(
            "LinkedIn redirected to the authentication wall instead of the public "
            f"company page. Target URL: {target_url}. "
            "The automation profile may need a one-time manual LinkedIn login, "
            "or LinkedIn may be blocking automated access on this machine."
        )

    expect(page).to_have_url(
        re.compile(re.escape(normalized_target) + r"/?", re.I),
        timeout=15000,
    )
