import re
import time

import allure
import pyautogui
import pytest
from playwright.sync_api import (
    Locator,
    Page,
    TimeoutError as PlaywrightTimeoutError,
    expect,
)

from pages.base_page import BasePage
from utils.chrome_toolbar import native_left_click
from utils.config import Config
from utils.marketplace_page import dismiss_marketplace_obstructions


class DakotaSidebarPage(BasePage):
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
    FIRM_RECORD_TYPE_LABEL = "Firm"
    ALLOCATOR_RECORD_TYPE_LABEL = "Allocator"
    LOAD_MORE_BUTTON_SELECTOR = "button:has-text('Load more')"
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
    INVESTORS_PAGE_SELECTOR = ".dakota-investors-page"
    INVESTORS_SCROLL_CONTAINER_SELECTORS = (
        ".dakota-investors-page",
        ".dakota-sidebar-body",
        ".dakota-loggedin-body",
        ".dakota-sidebar-content",
    )
    INVESTMENT_DETAILS_TAB_NAME = "Investment Details"
    INVESTMENT_DETAILS_TAB_SELECTOR = (
        'a.dakota-tab-button[href*="/investment-details"]'
    )
    INVESTMENT_DETAILS_NO_CONTENT_TEXT = "No investment information available"
    INVESTMENT_DETAILS_ITEM_SELECTOR = ".dakota-investment-details-item"
    INVESTMENT_DETAILS_DESCRIPTION_SELECTOR = ".dakota-investment-description"
    INVESTMENT_DETAILS_GEOGRAPHY_LABEL = "Geography"
    INVESTMENT_DETAILS_INDUSTRY_LABEL = "Industry"
    INVESTMENT_DETAILS_CHECK_SIZE_LABEL = "Check Size"
    INVESTMENT_DETAILS_PAGE_SELECTOR = ".dakota-investment-details-page"
    PLATFORM_DETAILS_TAB_NAME = "Platform Details"
    PLATFORM_DETAILS_TAB_SELECTOR = (
        'a.dakota-tab-button[href*="/platform-details"]'
    )
    PLATFORM_DETAILS_ITEM_SELECTOR = ".dakota-platform-info-item"
    PLATFORM_DETAILS_DESCRIPTION_SELECTOR = ".dakota-platform-description"
    PLATFORM_DETAILS_PLATFORM_DESCRIPTION_LABEL = "Platform Description"
    CONTACT_ITEM_SELECTOR = ".contacts-dakota-record-item"
    CONTACT_ROLE_SELECTOR = ".contacts-dakota-record-subDetails"
    CONTACT_URL_LINK_SELECTOR = "a.contacts-dakota-contact-link"
    CONTACT_EMAIL_SELECTOR = ".contacts-dakota-contact-email"
    CONTACT_EMAIL_LINK_SELECTOR = (
        ".contacts-dakota-contact-email a.contacts-dakota-contact-link"
    )
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
    ACCOUNT_OVERVIEW_CONTENT_SELECTOR = (
        "h3:has-text('Account Overview') ~ p"
    )
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

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    def login_to_dakota_marketplace(
        self,
        marketplace_url: str,
        username: str,
        password: str,
    ) -> None:
        """Open Dakota Marketplace, open the extension sidebar, and log in when required."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)

    def verify_dakota_search_results(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open sidebar, ensure login, search, and verify results plus API response."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)

    def verify_dakota_search_results_scroll(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open sidebar, search, and verify results can be scrolled to the end."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.scroll_search_results_to_end(search_term)

    def verify_dakota_search_results_load_more(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open sidebar, search, scroll, then load and verify more results."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.scroll_search_results_to_end(search_term)
        self.load_more_search_results(search_term)

    def verify_dakota_company_details(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open sidebar, search, open a result, and verify company details."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_search_result_and_verify_company_details(search_term)

    def verify_dakota_company_general_tab(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open sidebar, search, open a result, and verify General tab stat cards."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_stat_cards()

    def verify_dakota_contacts_count_matches_general_tab(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Contacts tab count matches General tab stat."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_count_matches_general_tab()

    def verify_dakota_company_account_overview(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Account Overview on the General tab."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_account_overview()

    def verify_dakota_company_general_tab_type(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Type is displayed on the General tab."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_type()

    def verify_dakota_company_general_tab_metro_area(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Metro Area is displayed on the General tab."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_metro_area()

    def verify_dakota_company_general_tab_website(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Website is displayed on the General tab."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_website()

    def verify_dakota_company_general_tab_linkedin_url(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify LinkedIn Url is displayed on the General tab."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_linkedin_url()

    def verify_dakota_company_general_tab_billing_address(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Billing Address is displayed on the General tab."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_general_tab_billing_address()

    def verify_dakota_company_investors_tab(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a private company and verify the Investors tab is available."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_company_investors_tab()

    def verify_dakota_company_investment_details_tab(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a Firm result and verify the Investment Details tab is available."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_firm_search_result()
        self.verify_company_investment_details_tab()

    def verify_dakota_company_platform_details_tab(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open an Allocator result and verify the Platform Details tab is available."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_allocator_search_result()
        self.verify_company_platform_details_tab()

    def verify_dakota_platform_details_tab_platform_description(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Platform Details displays Platform Description."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_platform_details_tab_platform_description()

    def verify_dakota_contacts_tab_results(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify the Contacts tab shows contacts or empty state."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_results()

    def verify_dakota_contacts_tab_contact_count(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify the Contacts tab shows the contact count."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_count()

    def verify_dakota_contacts_tab_load_more_button(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Contacts Load more matches General tab count."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_load_more_button()

    def verify_dakota_contacts_tab_load_more_displays_more(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Load more displays additional contacts."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_load_more_displays_more()

    def verify_dakota_contacts_tab_contact_roles(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify all contacts display a role."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_roles()

    def verify_dakota_contacts_tab_contact_urls(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify all contacts display a URL."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_urls()

    def verify_dakota_contacts_tab_contact_emails(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify all contacts display an email address."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_emails()

    def verify_dakota_contacts_tab_search_results(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        company_search_term: str,
        contact_search_term: str,
    ) -> None:
        """Open a company and verify the Contacts search bar returns results."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(company_search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_search_results(contact_search_term)

    def verify_dakota_contacts_tab_contact_details(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company, click the first contact, and verify details are displayed."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_details()

    def verify_dakota_contacts_tab_contact_type(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company, click the first contact, and verify Contact Type is displayed."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_type()

    def verify_dakota_contacts_tab_contact_metro_area(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company, click the first contact, and verify Metro Area is displayed."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_metro_area()

    def verify_dakota_contacts_tab_contact_phone(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company, click the first contact, and verify Phone is displayed."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_phone()

    def verify_dakota_contacts_tab_contact_detail_email(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company, click the first contact, and verify Email is displayed."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_detail_email()

    def verify_dakota_contacts_tab_contact_detail_linkedin_url(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company, click the first contact, and verify LinkedIn URL is displayed."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_contact_detail_linkedin_url()

    def verify_dakota_contacts_tab_go_back_to_contact_list(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a contact and verify Go back to contact list returns to the contacts list."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_contacts_tab_go_back_to_contact_list()

    def verify_dakota_investors_tab_results(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify the Investors tab shows results or empty state."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_results()

    def verify_dakota_investment_details_tab_details(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a Firm result and verify Investment Details shows data or empty state."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_firm_search_result()
        self.verify_investment_details_tab_details()

    def verify_dakota_investment_details_tab_geography(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a Firm result and verify Investment Details displays Geography."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_firm_search_result()
        self.verify_investment_details_tab_geography()

    def verify_dakota_investment_details_tab_industry(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a Firm result and verify Investment Details displays Industry."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_firm_search_result()
        self.verify_investment_details_tab_industry()

    def verify_dakota_investment_details_tab_check_size(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a Firm result and verify Investment Details displays Check Size."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_firm_search_result()
        self.verify_investment_details_tab_check_size()

    def verify_dakota_investors_tab_investor_count(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify the Investors tab shows the investor count."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_investor_count()

    def verify_dakota_investors_tab_load_more_button(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Load More Investors on the Investors tab."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_load_more_button()

    def verify_dakota_investors_tab_load_more_displays_more(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify Load More Investors displays more investors."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_load_more_displays_more()

    def verify_dakota_investors_tab_investor_metro_areas(
        self,
        marketplace_url: str,
        username: str,
        password: str,
        search_term: str,
    ) -> None:
        """Open a company and verify all investors display a state/city."""
        self.open_marketplace_and_sidebar(marketplace_url)
        self.ensure_logged_in(username, password)
        self.search_and_verify_results(search_term)
        self.open_first_search_result()
        self.verify_investors_tab_investor_metro_areas()

    def open_marketplace_and_sidebar(self, marketplace_url: str) -> None:
        pages_before_navigation = self._snapshot_open_pages()

        with allure.step("Open Dakota Marketplace page"):
            self.open(marketplace_url)
            expect(self.page).to_have_url(re.compile(r".*dakota-marketplace.*", re.I))
            expect(self.page.locator("h1").first).to_be_visible(timeout=25000)
            dismiss_marketplace_obstructions(self.page)
            self._dismiss_premature_salesforce_tabs(pages_before_navigation)

        with allure.step("Open Dakota from the pinned extension icon in the Chrome toolbar"):
            self.open_from_extension_toolbar()

    def ensure_logged_in(self, username: str, password: str) -> Locator:
        with allure.step("Determine login state from the open sidebar"):
            is_logged_in = self._wait_for_sidebar_auth_state()

        if not is_logged_in:
            with allure.step("Click Login to Dakota inside the open sidebar"):
                login_button = self._sidebar().locator(self.LOGIN_BUTTON_SELECTOR).first
                expect(login_button).to_be_visible(timeout=10000)
                login_button.click()

            with allure.step("Complete Salesforce login"):
                login_page = self._wait_for_salesforce_login_page()
                self.submit_salesforce_login(login_page, username, password)
                self.wait_for_salesforce_auth(login_page)

                self.page.bring_to_front()
                expect(self._sidebar().locator(self.SEARCH_BAR_SELECTOR).first).to_be_visible(
                    timeout=120000,
                )

        with allure.step("Verify logged-in Dakota sidebar is ready"):
            return self.ensure_sidebar_ready()

    def search_and_verify_results(self, search_term: str) -> None:
        with allure.step(f"Search for '{search_term}' in the Dakota sidebar"):
            search_bar = self.ensure_sidebar_ready()

            def api_matches(response) -> bool:
                return (
                    Config.DAKOTA_SEARCH_API_URL in response.url
                    and response.status == Config.DAKOTA_SEARCH_EXPECTED_API_STATUS
                )

            with self.page.expect_response(api_matches, timeout=30000) as response_info:
                self._replace_input_value(search_bar, search_term)
                search_bar.press("Enter")

            response = response_info.value
            print(
                f"Dakota search API responded with {response.status}: {response.url}"
            )

        with allure.step("Verify search results are displayed in the sidebar"):
            self._verify_search_results_visible(search_term)

    def scroll_search_results_to_end(self, search_term: str) -> None:
        with allure.step("Scroll search results to the end of the list"):
            sidebar = self._sidebar()
            results = sidebar.locator(self.SEARCH_RESULT_ITEM_SELECTOR)
            expect(results.first).to_be_visible(timeout=15000)

            result_count = results.count()
            assert result_count >= 1, (
                f"Expected search results before scrolling for '{search_term}'."
            )

            scroll_before = self._read_results_scroll_metrics(sidebar)
            print(
                "Scroll metrics before: "
                f"top={scroll_before['scrollTop']}, "
                f"height={scroll_before['scrollHeight']}, "
                f"viewport={scroll_before['clientHeight']}"
            )

            if result_count > 1:
                results.last.scroll_into_view_if_needed(timeout=15000)

            self._scroll_results_container_to_end(sidebar)
            self.page.wait_for_timeout(1000)

            scroll_after = self._read_results_scroll_metrics(sidebar)
            print(
                "Scroll metrics after: "
                f"top={scroll_after['scrollTop']}, "
                f"height={scroll_after['scrollHeight']}, "
                f"viewport={scroll_after['clientHeight']}"
            )

        with allure.step("Verify search results scrolled to the end"):
            self._verify_results_scrolled_to_end(scroll_before, scroll_after)
            if result_count > 1:
                expect(results.last).to_be_in_viewport(timeout=5000)

    def load_more_search_results(self, search_term: str) -> None:
        with allure.step('Click "Load more" to fetch additional search results'):
            sidebar = self._sidebar()
            results = sidebar.locator(self.SEARCH_RESULT_ITEM_SELECTOR)
            result_count_before = results.count()
            assert result_count_before >= 1, (
                f"Expected search results before Load more for '{search_term}'."
            )

            load_more_button = self._load_more_button(sidebar)
            expect(load_more_button).to_be_visible(timeout=10000)

            print(
                f"Search result count before Load more: {result_count_before}",
                flush=True,
            )

            def api_matches(response) -> bool:
                return (
                    Config.DAKOTA_SEARCH_API_URL in response.url
                    and response.status == Config.DAKOTA_SEARCH_EXPECTED_API_STATUS
                )

            with self.page.expect_response(api_matches, timeout=30000) as response_info:
                load_more_button.click()

            response = response_info.value
            print(
                f"Load more API responded with {response.status}: {response.url}",
                flush=True,
            )
            self.page.wait_for_timeout(3000)

        with allure.step("Verify additional search results are displayed"):
            sidebar = self._sidebar()
            results = sidebar.locator(self.SEARCH_RESULT_ITEM_SELECTOR)
            deadline = time.time() + 15
            while time.time() < deadline:
                if results.count() > result_count_before:
                    break
                time.sleep(0.5)

            result_count_after = results.count()
            print(
                f"Search result count after Load more: {result_count_after}",
                flush=True,
            )
            assert result_count_after > result_count_before, (
                f'Expected more results after clicking "Load more" for '
                f"'{search_term}', but count stayed at {result_count_after}."
            )
            expect(results.nth(result_count_before)).to_be_visible(timeout=10000)

    def _load_more_button(self, sidebar: Locator) -> Locator:
        role_based = sidebar.get_by_role("button", name=re.compile(r"load more", re.I))
        if role_based.count() > 0:
            return role_based.first
        return sidebar.locator(self.LOAD_MORE_BUTTON_SELECTOR).first

    def open_first_search_result(self) -> None:
        sidebar = self._sidebar()
        first_result = sidebar.locator(self.SEARCH_RESULT_ITEM_SELECTOR).first
        expect(first_result).to_be_visible(timeout=15000)

        with allure.step("Open the first search result"):
            def api_matches(response) -> bool:
                return (
                    Config.DAKOTA_SEARCH_API_URL in response.url
                    and response.status == Config.DAKOTA_SEARCH_EXPECTED_API_STATUS
                )

            with self.page.expect_response(api_matches, timeout=30000) as response_info:
                first_result.click()

            response = response_info.value
            print(
                f"Company detail API responded with {response.status}: {response.url}",
                flush=True,
            )
            self.page.wait_for_timeout(3000)

    def open_firm_search_result(self) -> None:
        sidebar = self._sidebar()
        firm_result = sidebar.locator(
            f"{self.SEARCH_RESULT_ITEM_SELECTOR}:has("
            f"{self.SEARCH_RESULT_TYPE_SELECTOR} "
            f"p:text-is('{self.FIRM_RECORD_TYPE_LABEL}'))"
        ).first
        expect(firm_result).to_be_visible(timeout=15000)

        with allure.step("Open the Firm search result"):
            def api_matches(response) -> bool:
                return (
                    Config.DAKOTA_SEARCH_API_URL in response.url
                    and response.status == Config.DAKOTA_SEARCH_EXPECTED_API_STATUS
                )

            with self.page.expect_response(api_matches, timeout=30000) as response_info:
                firm_result.click()

            response = response_info.value
            print(
                f"Firm detail API responded with {response.status}: {response.url}",
                flush=True,
            )
            self.page.wait_for_timeout(3000)

    def open_allocator_search_result(self) -> None:
        sidebar = self._sidebar()
        allocator_result = sidebar.locator(
            f"{self.SEARCH_RESULT_ITEM_SELECTOR}:has("
            f"{self.SEARCH_RESULT_TYPE_SELECTOR} "
            f"p:text-is('{self.ALLOCATOR_RECORD_TYPE_LABEL}'))"
        ).first
        expect(allocator_result).to_be_visible(timeout=15000)

        with allure.step("Open the Allocator search result"):
            def api_matches(response) -> bool:
                return (
                    Config.DAKOTA_SEARCH_API_URL in response.url
                    and response.status == Config.DAKOTA_SEARCH_EXPECTED_API_STATUS
                )

            with self.page.expect_response(api_matches, timeout=30000) as response_info:
                allocator_result.click()

            response = response_info.value
            print(
                f"Allocator detail API responded with {response.status}: {response.url}",
                flush=True,
            )
            self.page.wait_for_timeout(3000)

    def open_search_result_and_verify_company_details(self, search_term: str) -> None:
        self.open_first_search_result()

        with allure.step("Verify company details content is displayed"):
            self._verify_company_details_content_displayed(self._sidebar(), search_term)

    def verify_general_tab_stat_cards(self) -> None:
        with allure.step("Verify General tab stat cards are displayed"):
            sidebar = self._sidebar()
            expect(sidebar.locator(self.STATS_GRID_SELECTOR)).to_be_visible(timeout=15000)

            for label in self.GENERAL_TAB_STAT_LABELS:
                stat_value = self._get_general_tab_stat_value(sidebar, label)
                assert stat_value, f"Expected a displayed count for {label}."
                print(f"General tab {label}: {stat_value}", flush=True)

    def verify_general_tab_account_overview(self) -> None:
        with allure.step("Verify Account Overview heading is displayed"):
            sidebar = self._sidebar()
            overview_heading = sidebar.get_by_role(
                "heading",
                name=re.compile(r"Account Overview", re.I),
            )
            expect(overview_heading).to_be_visible(timeout=15000)

        with allure.step("Verify Account Overview content is displayed"):
            overview_content = sidebar.locator(self.ACCOUNT_OVERVIEW_CONTENT_SELECTOR).first
            expect(overview_content).to_be_visible(timeout=15000)
            content_text = overview_content.inner_text().strip()
            assert len(content_text) >= 20, (
                "Account Overview section did not display meaningful content."
            )
            print(
                f"Account Overview displayed ({len(content_text)} characters)",
                flush=True,
            )

    def verify_general_tab_type(self) -> None:
        with allure.step("Verify Type label is displayed on General tab"):
            sidebar = self._sidebar()
            type_label = sidebar.locator(self.INFO_LABEL_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.TYPE_LABEL)}$")
            ).first
            expect(type_label).to_be_visible(timeout=15000)

        with allure.step("Verify Type value is displayed on General tab"):
            type_value = self._get_general_tab_info_value(sidebar, self.TYPE_LABEL)
            assert type_value, "Expected a displayed Type value on the General tab."
            print(f"General tab Type: {type_value}", flush=True)

    def verify_general_tab_metro_area(self) -> None:
        with allure.step("Verify Metro Area label is displayed on General tab"):
            sidebar = self._sidebar()
            metro_area_label = sidebar.locator(self.INFO_LABEL_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.METRO_AREA_LABEL)}$")
            ).first
            expect(metro_area_label).to_be_visible(timeout=15000)

        with allure.step("Verify Metro Area value is displayed on General tab"):
            metro_area_value = self._get_general_tab_info_value(
                sidebar,
                self.METRO_AREA_LABEL,
            )
            assert metro_area_value, (
                "Expected a displayed Metro Area value on the General tab."
            )
            print(f"General tab Metro Area: {metro_area_value}", flush=True)

    def verify_general_tab_website(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Scroll General tab until Website is visible"):
            self._ensure_general_tab_info_label_visible(sidebar, self.WEBSITE_LABEL)
            self.page.wait_for_timeout(3000)

        with allure.step("Verify Website value is displayed on General tab"):
            website_value = self._get_general_tab_info_value(sidebar, self.WEBSITE_LABEL)
            assert website_value, "Expected a displayed Website value on the General tab."
            print(f"General tab Website: {website_value}", flush=True)

    def verify_general_tab_linkedin_url(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Scroll General tab until LinkedIn Url is visible"):
            self._ensure_general_tab_info_label_visible(sidebar, self.LINKEDIN_URL_LABEL)
            self.page.wait_for_timeout(3000)

        with allure.step("Verify LinkedIn Url value is displayed on General tab"):
            linkedin_url_value = self._get_general_tab_info_value(
                sidebar,
                self.LINKEDIN_URL_LABEL,
            )
            assert linkedin_url_value, (
                "Expected a displayed LinkedIn Url value on the General tab."
            )
            print(f"General tab LinkedIn Url: {linkedin_url_value}", flush=True)

    def verify_general_tab_billing_address(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Scroll General tab until Billing Address is visible"):
            self._ensure_general_tab_info_label_visible(
                sidebar,
                self.BILLING_ADDRESS_LABEL,
            )
            self.page.wait_for_timeout(3000)

        with allure.step("Verify Billing Address value is displayed on General tab"):
            billing_address_value = self._get_general_tab_info_value(
                sidebar,
                self.BILLING_ADDRESS_LABEL,
            )
            assert billing_address_value, (
                "Expected a displayed Billing Address value on the General tab."
            )
            print(
                f"General tab Billing Address: {billing_address_value}",
                flush=True,
            )

    def verify_company_investors_tab(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investors tab is displayed"):
            investors_tab = sidebar.locator(self.INVESTORS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.INVESTORS_TAB_NAME)}$")
            ).first
            expect(investors_tab).to_be_visible(timeout=15000)
            print(f"{self.INVESTORS_TAB_NAME} tab is displayed.", flush=True)

        with allure.step("Navigate to Investors tab"):
            self._open_investors_tab(sidebar)

    def verify_investors_tab_results(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investors tab is displayed"):
            investors_tab = sidebar.locator(self.INVESTORS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.INVESTORS_TAB_NAME)}$")
            ).first
            expect(investors_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Investors tab"):
            self._open_investors_tab(sidebar)

        with allure.step("Verify Investors tab displays results or empty state"):
            self._verify_investors_tab_content_displayed(sidebar)

    def verify_investors_tab_investor_count(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investors tab is displayed"):
            investors_tab = sidebar.locator(self.INVESTORS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.INVESTORS_TAB_NAME)}$")
            ).first
            expect(investors_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Investors tab"):
            self._open_investors_tab(sidebar)

        with allure.step("Verify Investors tab shows number of investors displayed"):
            self._verify_investors_tab_count_displayed(sidebar)

    def verify_investors_tab_load_more_button(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investors tab is displayed"):
            investors_tab = sidebar.locator(self.INVESTORS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.INVESTORS_TAB_NAME)}$")
            ).first
            expect(investors_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Investors tab"):
            self._open_investors_tab(sidebar)

        with allure.step("Scroll Investors tab until Load More Investors is visible"):
            load_more_button = self._ensure_load_more_investors_button_visible(sidebar)
            expect(load_more_button).to_be_visible(timeout=15000)
            print(
                f"{self.LOAD_MORE_INVESTORS_BUTTON_TEXT} button is visible.",
                flush=True,
            )

    def verify_investors_tab_load_more_displays_more(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investors tab is displayed"):
            investors_tab = sidebar.locator(self.INVESTORS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.INVESTORS_TAB_NAME)}$")
            ).first
            expect(investors_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Investors tab"):
            self._open_investors_tab(sidebar)

        with allure.step("Scroll Investors tab until Load More Investors is visible"):
            load_more_button = self._ensure_load_more_investors_button_visible(sidebar)
            expect(load_more_button).to_be_visible(timeout=15000)

        with allure.step(
            'Click "Load More Investors" to fetch additional investors'
        ):
            self._load_more_investors(sidebar)

        with allure.step("Scroll Investors tab to the end of the list"):
            self.scroll_investors_tab_to_end(sidebar)

    def verify_investors_tab_investor_metro_areas(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investors tab is displayed"):
            investors_tab = sidebar.locator(self.INVESTORS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.INVESTORS_TAB_NAME)}$")
            ).first
            expect(investors_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Investors tab"):
            self._open_investors_tab(sidebar)

        with allure.step("Scroll Investors tab until Load More Investors is visible"):
            load_more_button = self._ensure_load_more_investors_button_visible(sidebar)
            expect(load_more_button).to_be_visible(timeout=15000)

        with allure.step("Verify all investors on the page display a state/city"):
            self._verify_investors_metro_areas_displayed(sidebar)

    def verify_company_investment_details_tab(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investment Details tab is displayed"):
            investment_details_tab = sidebar.locator(
                self.INVESTMENT_DETAILS_TAB_SELECTOR
            ).filter(
                has_text=re.compile(r"^Investment\s+Details$", re.I)
            ).first
            expect(investment_details_tab).to_be_visible(timeout=15000)
            print(
                f"{self.INVESTMENT_DETAILS_TAB_NAME} tab is displayed.",
                flush=True,
            )

        with allure.step("Navigate to Investment Details tab"):
            self._open_investment_details_tab(sidebar)

    def verify_investment_details_tab_details(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investment Details tab is displayed"):
            investment_details_tab = sidebar.locator(
                self.INVESTMENT_DETAILS_TAB_SELECTOR
            ).filter(
                has_text=re.compile(r"^Investment\s+Details$", re.I)
            ).first
            expect(investment_details_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Investment Details tab"):
            self._open_investment_details_tab(sidebar)

        with allure.step(
            "Verify Investment Details tab displays data or empty state"
        ):
            self._verify_investment_details_tab_content_displayed(sidebar)

    def verify_investment_details_tab_geography(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investment Details tab is displayed"):
            investment_details_tab = sidebar.locator(
                self.INVESTMENT_DETAILS_TAB_SELECTOR
            ).filter(
                has_text=re.compile(r"^Investment\s+Details$", re.I)
            ).first
            expect(investment_details_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Investment Details tab"):
            self._open_investment_details_tab(sidebar)

        with allure.step("Verify Investment Details tab displays Geography"):
            self._verify_investment_details_geography_displayed(sidebar)

    def verify_investment_details_tab_industry(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investment Details tab is displayed"):
            investment_details_tab = sidebar.locator(
                self.INVESTMENT_DETAILS_TAB_SELECTOR
            ).filter(
                has_text=re.compile(r"^Investment\s+Details$", re.I)
            ).first
            expect(investment_details_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Investment Details tab"):
            self._open_investment_details_tab(sidebar)

        with allure.step("Verify Investment Details tab displays Industry"):
            self._verify_investment_details_industry_displayed(sidebar)

    def verify_investment_details_tab_check_size(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Investment Details tab is displayed"):
            investment_details_tab = sidebar.locator(
                self.INVESTMENT_DETAILS_TAB_SELECTOR
            ).filter(
                has_text=re.compile(r"^Investment\s+Details$", re.I)
            ).first
            expect(investment_details_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Investment Details tab"):
            self._open_investment_details_tab(sidebar)

        with allure.step("Verify Investment Details tab displays Check Size"):
            self._verify_investment_details_check_size_displayed(sidebar)

    def verify_company_platform_details_tab(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Platform Details tab is displayed"):
            platform_details_tab = sidebar.locator(
                self.PLATFORM_DETAILS_TAB_SELECTOR
            ).filter(
                has_text=re.compile(r"^Platform\s+Details$", re.I)
            ).first
            expect(platform_details_tab).to_be_visible(timeout=15000)
            print(
                f"{self.PLATFORM_DETAILS_TAB_NAME} tab is displayed.",
                flush=True,
            )

        with allure.step("Navigate to Platform Details tab"):
            self._open_platform_details_tab(sidebar)

    def verify_platform_details_tab_platform_description(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Platform Details tab is displayed"):
            platform_details_tab = sidebar.locator(
                self.PLATFORM_DETAILS_TAB_SELECTOR
            ).filter(
                has_text=re.compile(r"^Platform\s+Details$", re.I)
            ).first
            expect(platform_details_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Platform Details tab"):
            self._open_platform_details_tab(sidebar)

        with allure.step("Verify Platform Details tab displays Platform Description"):
            self._verify_platform_details_platform_description_displayed(sidebar)

    def verify_contacts_tab_results(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Verify Contacts tab displays contacts or empty state"):
            self._verify_contacts_tab_content_displayed(sidebar)

    def verify_contacts_tab_contact_roles(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Verify all contacts on the page display a role"):
            self._verify_contacts_tab_roles_displayed(sidebar)

    def verify_contacts_tab_contact_urls(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Verify all contacts on the page display a URL"):
            self._verify_contacts_tab_urls_displayed(sidebar)

    def verify_contacts_tab_contact_emails(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Verify all contacts on the page display an email address"):
            self._verify_contacts_tab_emails_displayed(sidebar)

    def verify_contacts_tab_search_results(self, contact_search_term: str) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step(
            f"Search contacts for '{contact_search_term}' and verify results"
        ):
            self._search_contacts_and_verify_results(sidebar, contact_search_term)

    def verify_contacts_tab_contact_details(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Click the first contact and verify details are displayed"):
            contact_name = self._open_first_contact_details(sidebar)
            self._verify_contact_details_displayed(sidebar, contact_name)

    def verify_contacts_tab_contact_type(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Click the first contact and verify Contact Type is displayed"):
            self._open_first_contact_details(sidebar)
            self._verify_contact_detail_contact_type_displayed(sidebar)

    def verify_contacts_tab_contact_metro_area(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Click the first contact and verify Metro Area is displayed"):
            self._open_first_contact_details(sidebar)
            self._verify_contact_detail_metro_area_displayed(sidebar)

    def verify_contacts_tab_contact_phone(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Click the first contact and verify Phone is displayed"):
            self._open_first_contact_details(sidebar)
            self._verify_contact_detail_phone_displayed(sidebar)

    def verify_contacts_tab_contact_detail_email(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Click the first contact and verify Email is displayed"):
            self._open_first_contact_details(sidebar)
            self._verify_contact_detail_email_displayed(sidebar)

    def verify_contacts_tab_contact_detail_linkedin_url(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step(
            "Click the first contact, scroll to LinkedIn URL if needed, "
            "and verify it is displayed"
        ):
            self._open_first_contact_details(sidebar)
            self._verify_contact_detail_linkedin_url_displayed(sidebar)

    def verify_contacts_tab_go_back_to_contact_list(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Open the first contact details page"):
            self._open_first_contact_details(sidebar)

        with allure.step(
            f'Click "{self.CONTACT_DETAIL_BACK_BUTTON_TEXT}" and verify contacts list'
        ):
            self._go_back_to_contacts_list(sidebar)
            self._verify_contacts_list_displayed(sidebar)

    def verify_contacts_tab_contact_count(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Verify Contacts tab shows number of results displayed"):
            self._verify_contacts_tab_count_displayed(sidebar)

    def verify_contacts_tab_load_more_button(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Read Contacts count on General tab"):
            general_contacts_value = self._get_general_tab_stat_value(
                sidebar,
                self.CONTACTS_TAB_NAME,
            )
            general_contacts_count = self._parse_contacts_stat_count(
                general_contacts_value
            )
            print(
                f"General tab Contacts count: {general_contacts_value} "
                f"({general_contacts_count})",
                flush=True,
            )

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Scroll Contacts tab to the end of the list"):
            self.scroll_contacts_tab_to_end(sidebar)

        with allure.step(
            "Verify Load more button visibility matches General tab contact count"
        ):
            self._verify_contacts_tab_load_more_visibility(
                sidebar,
                general_contacts_count,
            )

    def verify_contacts_tab_load_more_displays_more(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Read Contacts count on General tab"):
            general_contacts_value = self._get_general_tab_stat_value(
                sidebar,
                self.CONTACTS_TAB_NAME,
            )
            general_contacts_count = self._parse_contacts_stat_count(
                general_contacts_value
            )
            print(
                f"General tab Contacts count: {general_contacts_value} "
                f"({general_contacts_count})",
                flush=True,
            )
            assert general_contacts_count > self.CONTACTS_PAGE_SIZE, (
                f"Expected more than {self.CONTACTS_PAGE_SIZE} contacts to verify "
                f"Load more displays more, but General tab shows "
                f"{general_contacts_count}."
            )

        with allure.step("Verify Contacts tab is displayed"):
            contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
                has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
            ).first
            expect(contacts_tab).to_be_visible(timeout=15000)

        with allure.step("Navigate to Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Scroll Contacts tab until Load more is visible"):
            self.scroll_contacts_tab_to_end(sidebar)
            load_more_button = sidebar.locator(
                self.CONTACTS_LOAD_MORE_BUTTON_SELECTOR
            )
            if load_more_button.count() == 0:
                load_more_button = self._ensure_load_more_contacts_button_visible(
                    sidebar
                )
            else:
                load_more_button = load_more_button.first
                load_more_button.scroll_into_view_if_needed(timeout=5000)
            expect(load_more_button).to_be_visible(timeout=15000)

        with allure.step('Click "Load more" to fetch additional contacts'):
            self._load_more_contacts(sidebar)

        with allure.step("Scroll Contacts tab to the end of the list"):
            self.scroll_contacts_tab_to_end(sidebar)

    def verify_contacts_count_matches_general_tab(self) -> None:
        sidebar = self._sidebar()

        with allure.step("Read Contacts count on General tab"):
            general_contacts_value = self._get_general_tab_stat_value(
                sidebar,
                self.CONTACTS_TAB_NAME,
            )
            general_contacts_count = self._parse_contacts_stat_count(general_contacts_value)
            print(
                f"General tab Contacts count: {general_contacts_value} "
                f"({general_contacts_count})",
                flush=True,
            )

        with allure.step("Open Contacts tab"):
            self._open_contacts_tab(sidebar)

        with allure.step("Verify Contacts tab count matches General tab"):
            contacts_tab_count = self._count_contacts_on_contacts_tab(sidebar)
            print(f"Contacts tab displayed count: {contacts_tab_count}", flush=True)
            assert contacts_tab_count == general_contacts_count, (
                "Contacts tab count does not match General tab Contacts stat. "
                f"General tab: {general_contacts_count}, Contacts tab: {contacts_tab_count}"
            )

    def _get_general_tab_stat_value(self, sidebar: Locator, label: str) -> str:
        stats_grid = sidebar.locator(self.STATS_GRID_SELECTOR)
        stat_item = stats_grid.locator(self.STAT_ITEM_SELECTOR).filter(
            has_text=label
        ).first
        expect(stat_item).to_be_visible(timeout=10000)
        stat_number = stat_item.locator(self.STAT_NUMBER_SELECTOR)
        expect(stat_number).to_be_visible()
        return stat_number.inner_text().strip()

    def _get_general_tab_info_value(self, sidebar: Locator, label: str) -> str:
        info_value = sidebar.locator(
            f"{self.INFO_LABEL_SELECTOR}:has-text('{label}') + {self.INFO_VALUE_SELECTOR}"
        ).first
        expect(info_value).to_be_visible(timeout=10000)
        return info_value.inner_text().strip()

    def _ensure_general_tab_info_label_visible(
        self,
        sidebar: Locator,
        label: str,
    ) -> Locator:
        info_label = sidebar.locator(self.INFO_LABEL_SELECTOR).filter(
            has_text=re.compile(rf"^{re.escape(label)}$")
        ).first
        expect(info_label).to_be_attached(timeout=15000)

        scroll_before = self._read_general_tab_scroll_metrics(info_label)
        print(
            "General tab scroll before: "
            f"top={scroll_before['scrollTop']}, "
            f"height={scroll_before['scrollHeight']}, "
            f"viewport={scroll_before['clientHeight']}",
            flush=True,
        )

        if not self._is_info_label_in_scroll_viewport(info_label):
            for attempt in range(60):
                if self._is_info_label_in_scroll_viewport(info_label):
                    break

                scrolled = self._scroll_info_label_toward_viewport(info_label)
                if not scrolled:
                    self._wheel_scroll_general_tab_down(sidebar)
                self.page.wait_for_timeout(200)

                if attempt % 10 == 9:
                    print(
                        f"General tab scroll attempt {attempt + 1}: "
                        f"{self._read_general_tab_scroll_metrics(info_label)}",
                        flush=True,
                    )

        info_label.evaluate(
            "node => node.scrollIntoView({ block: 'center', inline: 'nearest' })"
        )
        self.page.wait_for_timeout(300)

        if not self._is_info_label_in_scroll_viewport(info_label):
            self._wheel_scroll_general_tab_down(sidebar)
            info_label.evaluate(
                "node => node.scrollIntoView({ block: 'center', inline: 'nearest' })"
            )

        expect(info_label).to_be_visible(timeout=15000)
        assert self._is_info_label_in_scroll_viewport(info_label), (
            f"{label} is not visible in the General tab viewport after scrolling."
        )

        scroll_after = self._read_general_tab_scroll_metrics(info_label)
        print(
            "General tab scroll after: "
            f"top={scroll_after['scrollTop']}, "
            f"height={scroll_after['scrollHeight']}, "
            f"viewport={scroll_after['clientHeight']}",
            flush=True,
        )
        return info_label

    def _find_scrollable_ancestor(self, target: Locator) -> dict[str, int | str]:
        return target.evaluate(
            """
            (node) => {
                const isScrollable = (element) => {
                    const style = window.getComputedStyle(element);
                    const overflowY = style.overflowY;
                    return (
                        (overflowY === 'auto' || overflowY === 'scroll')
                        && element.scrollHeight > element.clientHeight + 1
                    );
                };

                let current = node.parentElement;
                while (current) {
                    if (isScrollable(current)) {
                        return {
                            scrollTop: current.scrollTop,
                            scrollHeight: current.scrollHeight,
                            clientHeight: current.clientHeight,
                            className: current.className || '',
                        };
                    }
                    current = current.parentElement;
                }

                return {
                    scrollTop: 0,
                    scrollHeight: 0,
                    clientHeight: 0,
                    className: '',
                };
            }
            """
        )

    def _read_general_tab_scroll_metrics(self, target: Locator) -> dict[str, int]:
        metrics = self._find_scrollable_ancestor(target)
        return {
            "scrollTop": int(metrics["scrollTop"]),
            "scrollHeight": int(metrics["scrollHeight"]),
            "clientHeight": int(metrics["clientHeight"]),
        }

    def _is_info_label_in_scroll_viewport(self, target: Locator) -> bool:
        if target.count() == 0 or not target.is_visible():
            return False

        return target.evaluate(
            """
            (node) => {
                const isScrollable = (element) => {
                    const style = window.getComputedStyle(element);
                    const overflowY = style.overflowY;
                    return (
                        (overflowY === 'auto' || overflowY === 'scroll')
                        && element.scrollHeight > element.clientHeight + 1
                    );
                };

                const rect = node.getBoundingClientRect();
                let current = node.parentElement;
                while (current) {
                    if (isScrollable(current)) {
                        const containerRect = current.getBoundingClientRect();
                        return (
                            rect.top >= containerRect.top
                            && rect.bottom <= containerRect.bottom
                            && rect.width > 0
                            && rect.height > 0
                        );
                    }
                    current = current.parentElement;
                }

                return (
                    rect.top >= 0
                    && rect.bottom <= window.innerHeight
                    && rect.width > 0
                    && rect.height > 0
                );
            }
            """
        )

    def _scroll_info_label_toward_viewport(self, target: Locator) -> bool:
        return target.evaluate(
            """
            (node) => {
                const isScrollable = (element) => {
                    const style = window.getComputedStyle(element);
                    const overflowY = style.overflowY;
                    return (
                        (overflowY === 'auto' || overflowY === 'scroll')
                        && element.scrollHeight > element.clientHeight + 1
                    );
                };

                let container = node.parentElement;
                while (container && !isScrollable(container)) {
                    container = container.parentElement;
                }
                if (!container) {
                    return false;
                }

                const rect = node.getBoundingClientRect();
                const containerRect = container.getBoundingClientRect();
                const previousScrollTop = container.scrollTop;

                if (rect.bottom > containerRect.bottom) {
                    container.scrollTop += rect.bottom - containerRect.bottom + 24;
                } else if (rect.top < containerRect.top) {
                    container.scrollTop -= containerRect.top - rect.top + 24;
                } else {
                    container.scrollTop = Math.min(
                        container.scrollTop + 300,
                        container.scrollHeight - container.clientHeight
                    );
                }

                return container.scrollTop !== previousScrollTop;
            }
            """
        )

    def _wheel_scroll_general_tab_down(self, sidebar: Locator) -> None:
        for selector in self.GENERAL_TAB_SCROLL_CONTAINER_SELECTORS:
            scroll_container = sidebar.locator(selector).first
            if scroll_container.count() == 0:
                continue

            metrics = self._read_scroll_container_metrics(scroll_container)
            if metrics["scrollHeight"] <= metrics["clientHeight"] + 1:
                continue

            scroll_container.hover(force=True, timeout=3000)
            self.page.mouse.wheel(0, 500)
            return

        sidebar.hover(force=True, timeout=3000)
        self.page.mouse.wheel(0, 500)

    def _read_scroll_container_metrics(self, scroll_container: Locator) -> dict[str, int]:
        return scroll_container.evaluate(
            """node => ({
                scrollTop: node.scrollTop,
                scrollHeight: node.scrollHeight,
                clientHeight: node.clientHeight,
            })"""
        )

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

    def _open_contacts_tab(self, sidebar: Locator) -> None:
        contacts_tab = sidebar.locator(self.CONTACTS_TAB_SELECTOR).filter(
            has_text=re.compile(rf"^{re.escape(self.CONTACTS_TAB_NAME)}$")
        ).first
        expect(contacts_tab).to_be_visible(timeout=10000)
        contacts_tab.click()
        self.page.wait_for_timeout(3000)
        print(f"Navigated to {self.CONTACTS_TAB_NAME} tab.", flush=True)

    def _verify_contacts_tab_content_displayed(self, sidebar: Locator) -> None:
        no_results = sidebar.locator(".dakota-no-results p").filter(
            has_text=re.compile(re.escape(self.CONTACTS_NO_RESULTS_TEXT), re.I)
        )
        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)

        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() > 0:
                break
            if no_results.count() > 0 and no_results.first.is_visible():
                break
            time.sleep(0.5)

        expect(no_results.or_(contact_items.first)).to_be_visible(timeout=15000)

        if no_results.count() > 0 and no_results.first.is_visible():
                print(
                f"Contacts tab displayed empty state: {self.CONTACTS_NO_RESULTS_TEXT}",
                flush=True,
            )
        else:
            expect(contact_items.first).to_be_visible(timeout=10000)
            contact_count = contact_items.count()
            print(
                f"Contacts tab displayed {contact_count} contact result(s).",
                flush=True,
            )

        self.page.wait_for_timeout(3000)

    def _verify_contacts_tab_roles_displayed(self, sidebar: Locator) -> None:
        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() > 0:
                break
            time.sleep(0.5)

        expect(contact_items.first).to_be_visible(timeout=15000)
        contact_count = contact_items.count()
        assert contact_count >= 1, (
            "Expected at least one contact to verify role display."
        )

        for index in range(contact_count):
            contact = contact_items.nth(index)
            role = contact.locator(self.CONTACT_ROLE_SELECTOR).first
            expect(role).to_be_visible(timeout=10000)
            role_text = role.inner_text().strip()
            assert role_text, (
                f"Contact {index + 1} of {contact_count} is missing a role."
            )
            print(
                f"Contact {index + 1} role: {role_text}",
                flush=True,
            )

        print(
            f"All {contact_count} contact(s) display a role.",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

    def _verify_contacts_tab_urls_displayed(self, sidebar: Locator) -> None:
        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() > 0:
                break
            time.sleep(0.5)

        expect(contact_items.first).to_be_visible(timeout=15000)
        contact_count = contact_items.count()
        assert contact_count >= 1, (
            "Expected at least one contact to verify URL display."
        )

        for index in range(contact_count):
            contact = contact_items.nth(index)
            url_link = contact.locator(self.CONTACT_URL_LINK_SELECTOR).first
            expect(url_link).to_be_visible(timeout=10000)
            url_href = (url_link.get_attribute("href") or "").strip()
            assert url_href, (
                f"Contact {index + 1} of {contact_count} is missing a URL href."
            )
            print(
                f"Contact {index + 1} URL: {url_href}",
                flush=True,
            )

        print(
            f"All {contact_count} contact(s) display a URL.",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

    def _verify_contacts_tab_emails_displayed(self, sidebar: Locator) -> None:
        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() > 0:
                break
            time.sleep(0.5)

        expect(contact_items.first).to_be_visible(timeout=15000)
        contact_count = contact_items.count()
        assert contact_count >= 1, (
            "Expected at least one contact to verify email display."
        )

        for index in range(contact_count):
            contact = contact_items.nth(index)
            email_block = contact.locator(self.CONTACT_EMAIL_SELECTOR)
            expect(email_block).to_be_visible(timeout=10000)

            email_link = contact.locator(self.CONTACT_EMAIL_LINK_SELECTOR).first
            expect(email_link).to_be_visible(timeout=10000)
            email_href = (email_link.get_attribute("href") or "").strip()
            assert email_href.lower().startswith("mailto:"), (
                f"Contact {index + 1} of {contact_count} is missing a mailto email "
                f"href. Found: {email_href!r}"
            )

            email_text = email_link.inner_text().strip()
            assert email_text, (
                f"Contact {index + 1} of {contact_count} is missing email text."
            )
            print(
                f"Contact {index + 1} email: {email_text}",
                flush=True,
            )

        print(
            f"All {contact_count} contact(s) display an email address.",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

    def _open_first_contact_details(self, sidebar: Locator) -> str:
        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() > 0:
                break
            time.sleep(0.5)

        expect(contact_items.first).to_be_visible(timeout=15000)
        first_contact = contact_items.first
        name_locator = first_contact.locator(self.CONTACT_NAME_SELECTOR).first
        expect(name_locator).to_be_visible(timeout=10000)
        contact_name = name_locator.inner_text().strip()
        assert contact_name, "Expected the first contact to have a name before opening details."

        first_contact.click()
        print(f"Clicked first contact: {contact_name}", flush=True)
        self.page.wait_for_timeout(2000)
        return contact_name

    def _verify_contact_details_displayed(
        self,
        sidebar: Locator,
        expected_contact_name: str,
    ) -> None:
        detail_page = sidebar.locator(self.CONTACT_DETAIL_PAGE_SELECTOR)
        expect(detail_page).to_be_visible(timeout=15000)

        detail_name = sidebar.locator(self.CONTACT_DETAIL_NAME_SELECTOR).first
        expect(detail_name).to_be_visible(timeout=10000)
        detail_name_text = detail_name.inner_text().strip()
        assert detail_name_text, "Contact detail page name is empty."
        assert detail_name_text.lower() == expected_contact_name.lower(), (
            f"Contact detail name '{detail_name_text}' does not match the "
            f"selected contact '{expected_contact_name}'."
        )

        detail_title = sidebar.locator(self.CONTACT_DETAIL_TITLE_SELECTOR).first
        detail_fields = sidebar.locator(self.CONTACT_DETAIL_FIELD_SELECTOR)
        title_text = ""
        if detail_title.count() > 0 and detail_title.is_visible():
            title_text = detail_title.inner_text().strip()

        field_count = detail_fields.count()
        populated_fields = 0
        for index in range(field_count):
            field = detail_fields.nth(index)
            label = field.locator(".contacts-dakota-detail-field-label").first
            value = field.locator(".contacts-dakota-detail-field-value").first
            if label.count() == 0 or value.count() == 0:
                continue
            label_text = label.inner_text().strip()
            value_text = value.inner_text().strip()
            if label_text and value_text:
                populated_fields += 1
                print(
                    f"Contact detail field: {label_text} = {value_text}",
                    flush=True,
                )

        assert title_text or populated_fields >= 1, (
            f"Contact detail page for '{detail_name_text}' has no loaded data."
        )

        if title_text:
            print(f"Contact detail title: {title_text}", flush=True)

        print(
            f"Contact detail page displayed data for '{detail_name_text}' "
            f"({populated_fields} field(s)).",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

    def _verify_contact_detail_contact_type_displayed(self, sidebar: Locator) -> None:
        detail_page = sidebar.locator(self.CONTACT_DETAIL_PAGE_SELECTOR)
        expect(detail_page).to_be_visible(timeout=15000)

        contact_type_field = sidebar.locator(
            f"{self.CONTACT_DETAIL_FIELD_SELECTOR}:has("
            f"{self.CONTACT_DETAIL_FIELD_LABEL_SELECTOR}"
            f':text-is("{self.CONTACT_DETAIL_CONTACT_TYPE_LABEL}"))'
        ).first
        expect(contact_type_field).to_be_visible(timeout=10000)

        contact_type_value = contact_type_field.locator(
            self.CONTACT_DETAIL_FIELD_VALUE_SELECTOR
        ).first
        expect(contact_type_value).to_be_visible(timeout=10000)
        contact_type_text = contact_type_value.inner_text().strip()
        assert contact_type_text, (
            f"{self.CONTACT_DETAIL_CONTACT_TYPE_LABEL} is displayed but has no value."
        )

        print(
            f"{self.CONTACT_DETAIL_CONTACT_TYPE_LABEL}: {contact_type_text}",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

    def _verify_contact_detail_metro_area_displayed(self, sidebar: Locator) -> None:
        detail_page = sidebar.locator(self.CONTACT_DETAIL_PAGE_SELECTOR)
        expect(detail_page).to_be_visible(timeout=15000)

        metro_area_field = sidebar.locator(
            f"{self.CONTACT_DETAIL_FIELD_SELECTOR}:has("
            f"{self.CONTACT_DETAIL_FIELD_LABEL_SELECTOR}"
            f':text-is("{self.CONTACT_DETAIL_METRO_AREA_LABEL}"))'
        ).first
        expect(metro_area_field).to_be_visible(timeout=10000)

        metro_area_value = metro_area_field.locator(
            self.CONTACT_DETAIL_FIELD_VALUE_SELECTOR
        ).first
        expect(metro_area_value).to_be_visible(timeout=10000)
        metro_area_text = metro_area_value.inner_text().strip()
        assert metro_area_text, (
            f"{self.CONTACT_DETAIL_METRO_AREA_LABEL} is displayed but has no value."
        )

        print(
            f"{self.CONTACT_DETAIL_METRO_AREA_LABEL}: {metro_area_text}",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

    def _verify_contact_detail_phone_displayed(self, sidebar: Locator) -> None:
        detail_page = sidebar.locator(self.CONTACT_DETAIL_PAGE_SELECTOR)
        expect(detail_page).to_be_visible(timeout=15000)

        phone_field = sidebar.locator(
            f"{self.CONTACT_DETAIL_FIELD_SELECTOR}:has("
            f"{self.CONTACT_DETAIL_FIELD_LABEL_SELECTOR}"
            f':text-is("{self.CONTACT_DETAIL_PHONE_LABEL}"))'
        ).first
        expect(phone_field).to_be_visible(timeout=10000)

        phone_value = phone_field.locator(self.CONTACT_DETAIL_FIELD_VALUE_SELECTOR).first
        expect(phone_value).to_be_visible(timeout=10000)
        phone_text = phone_value.inner_text().strip()
        assert phone_text, (
            f"{self.CONTACT_DETAIL_PHONE_LABEL} is displayed but has no value."
        )

        phone_link = phone_field.locator(
            f'a.contacts-dakota-detail-field-link[href^="tel:"]'
        ).first
        expect(phone_link).to_be_visible(timeout=10000)
        phone_href = (phone_link.get_attribute("href") or "").strip()
        assert phone_href.lower().startswith("tel:"), (
            f"{self.CONTACT_DETAIL_PHONE_LABEL} link is missing a tel: href. "
            f"Found: {phone_href!r}"
        )

        print(f"{self.CONTACT_DETAIL_PHONE_LABEL}: {phone_text}", flush=True)
        self.page.wait_for_timeout(3000)

    def _verify_contact_detail_email_displayed(self, sidebar: Locator) -> None:
        detail_page = sidebar.locator(self.CONTACT_DETAIL_PAGE_SELECTOR)
        expect(detail_page).to_be_visible(timeout=15000)

        email_field = sidebar.locator(
            f"{self.CONTACT_DETAIL_FIELD_SELECTOR}:has("
            f"{self.CONTACT_DETAIL_FIELD_LABEL_SELECTOR}"
            f':text-is("{self.CONTACT_DETAIL_EMAIL_LABEL}"))'
        ).first
        expect(email_field).to_be_visible(timeout=10000)

        email_value = email_field.locator(self.CONTACT_DETAIL_FIELD_VALUE_SELECTOR).first
        expect(email_value).to_be_visible(timeout=10000)
        email_text = email_value.inner_text().strip()
        assert email_text, (
            f"{self.CONTACT_DETAIL_EMAIL_LABEL} is displayed but has no value."
        )

        email_link = email_field.locator(
            'a.contacts-dakota-detail-field-link[href^="mailto:"]'
        ).first
        expect(email_link).to_be_visible(timeout=10000)
        email_href = (email_link.get_attribute("href") or "").strip()
        assert email_href.lower().startswith("mailto:"), (
            f"{self.CONTACT_DETAIL_EMAIL_LABEL} link is missing a mailto: href. "
            f"Found: {email_href!r}"
        )

        print(f"{self.CONTACT_DETAIL_EMAIL_LABEL}: {email_text}", flush=True)
        self.page.wait_for_timeout(3000)

    def _ensure_contact_detail_field_visible(
        self,
        sidebar: Locator,
        field_label: str,
    ) -> Locator:
        field = sidebar.locator(
            f"{self.CONTACT_DETAIL_FIELD_SELECTOR}:has("
            f"{self.CONTACT_DETAIL_FIELD_LABEL_SELECTOR}"
            f':text-is("{field_label}"))'
        ).first
        expect(field).to_be_attached(timeout=15000)

        if self._is_info_label_in_scroll_viewport(field):
            print(
                f"Contact detail {field_label} is already visible in the viewport.",
                flush=True,
            )
            return field

        scroll_before = self._read_general_tab_scroll_metrics(field)
        print(
            "Contact detail scroll before: "
            f"top={scroll_before['scrollTop']}, "
            f"height={scroll_before['scrollHeight']}, "
            f"viewport={scroll_before['clientHeight']}",
            flush=True,
        )

                for attempt in range(60):
            if self._is_info_label_in_scroll_viewport(field):
                break

            scrolled = self._scroll_info_label_toward_viewport(field)
            if not scrolled:
                self._wheel_scroll_general_tab_down(sidebar)
            self.page.wait_for_timeout(200)

            if attempt % 10 == 9:
                print(
                    f"Contact detail scroll attempt {attempt + 1}: "
                    f"{self._read_general_tab_scroll_metrics(field)}",
                    flush=True,
                )

        field.evaluate(
            "node => node.scrollIntoView({ block: 'center', inline: 'nearest' })"
        )
        self.page.wait_for_timeout(300)

        if not self._is_info_label_in_scroll_viewport(field):
            self._wheel_scroll_general_tab_down(sidebar)
            field.evaluate(
                "node => node.scrollIntoView({ block: 'center', inline: 'nearest' })"
            )

        expect(field).to_be_visible(timeout=15000)
        assert self._is_info_label_in_scroll_viewport(field), (
            f"{field_label} is not visible in the contact detail viewport "
            "after scrolling."
        )

        scroll_after = self._read_general_tab_scroll_metrics(field)
        print(
            "Contact detail scroll after: "
            f"top={scroll_after['scrollTop']}, "
            f"height={scroll_after['scrollHeight']}, "
            f"viewport={scroll_after['clientHeight']}",
            flush=True,
        )
        return field

    def _verify_contact_detail_linkedin_url_displayed(self, sidebar: Locator) -> None:
        detail_page = sidebar.locator(self.CONTACT_DETAIL_PAGE_SELECTOR)
        expect(detail_page).to_be_visible(timeout=15000)

        linkedin_field = self._ensure_contact_detail_field_visible(
            sidebar,
            self.CONTACT_DETAIL_LINKEDIN_URL_LABEL,
        )

        linkedin_value = linkedin_field.locator(
            self.CONTACT_DETAIL_FIELD_VALUE_SELECTOR
        ).first
        expect(linkedin_value).to_be_visible(timeout=10000)
        linkedin_text = linkedin_value.inner_text().strip()
        assert linkedin_text, (
            f"{self.CONTACT_DETAIL_LINKEDIN_URL_LABEL} is displayed but has no value."
        )

        linkedin_link = linkedin_field.locator(
            "a.contacts-dakota-detail-field-link"
        ).first
        expect(linkedin_link).to_be_visible(timeout=10000)
        linkedin_href = (linkedin_link.get_attribute("href") or "").strip()
        assert "linkedin.com" in linkedin_href.lower(), (
            f"{self.CONTACT_DETAIL_LINKEDIN_URL_LABEL} link is missing a LinkedIn "
            f"href. Found: {linkedin_href!r}"
        )

        print(
            f"{self.CONTACT_DETAIL_LINKEDIN_URL_LABEL}: {linkedin_href}",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

    def _go_back_to_contacts_list(self, sidebar: Locator) -> None:
        detail_page = sidebar.locator(self.CONTACT_DETAIL_PAGE_SELECTOR)
        expect(detail_page).to_be_visible(timeout=15000)
        self.page.wait_for_timeout(3000)

        back_button = sidebar.locator(self.CONTACT_DETAIL_BACK_BUTTON_SELECTOR).filter(
            has_text=re.compile(
                re.escape(self.CONTACT_DETAIL_BACK_BUTTON_TEXT), re.I
            )
        ).first
        expect(back_button).to_be_visible(timeout=10000)
        back_button.click()
        print(
            f'Clicked "{self.CONTACT_DETAIL_BACK_BUTTON_TEXT}".',
            flush=True,
        )
        self.page.wait_for_timeout(2000)

    def _verify_contacts_list_displayed(self, sidebar: Locator) -> None:
        expect(sidebar.locator(self.CONTACT_DETAIL_PAGE_SELECTOR)).not_to_be_visible(
            timeout=15000
        )

        search_input = sidebar.locator(self.CONTACTS_SEARCH_INPUT_SELECTOR).first
        expect(search_input).to_be_visible(timeout=10000)

        contacts_header = sidebar.locator(self.CONTACTS_HEADER_SELECTOR)
        expect(contacts_header.locator("h3")).to_have_text(
            self.CONTACTS_TAB_NAME,
            timeout=15000,
        )

        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() > 0:
                                    break
            time.sleep(0.5)

        expect(contact_items.first).to_be_visible(timeout=15000)
        contact_count = contact_items.count()
        assert contact_count >= 1, (
            "Expected the contacts list to display at least one contact."
        )
        print(
            f"Contacts list displayed {contact_count} contact(s).",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

    def _search_contacts_and_verify_results(
        self,
        sidebar: Locator,
        contact_search_term: str,
    ) -> None:
        search_input = sidebar.locator(self.CONTACTS_SEARCH_INPUT_SELECTOR).first
        expect(search_input).to_be_visible(timeout=10000)
        print(
            f"Searching contacts for '{contact_search_term}'.",
            flush=True,
        )

        def api_matches(response) -> bool:
            return (
                Config.DAKOTA_SEARCH_API_URL in response.url
                and response.status == Config.DAKOTA_SEARCH_EXPECTED_API_STATUS
            )

        with self.page.expect_response(api_matches, timeout=30000) as response_info:
            self._replace_input_value(search_input, contact_search_term)

        response = response_info.value
        print(
            f"Contacts search API responded with {response.status}: {response.url}",
            flush=True,
        )

        loading = sidebar.locator(".contacts-dakota-loading")
        deadline = time.time() + 15
        while time.time() < deadline:
            if loading.count() == 0 or not loading.first.is_visible():
                break
            time.sleep(0.5)

        self._verify_contacts_search_results_displayed(sidebar, contact_search_term)

    def _verify_contacts_search_results_displayed(
        self,
        sidebar: Locator,
        contact_search_term: str,
    ) -> None:
        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        no_results = sidebar.locator(".contacts-dakota-no-results p").filter(
            has_text=re.compile(re.escape(self.CONTACTS_NO_RESULTS_TEXT), re.I)
        )

        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() > 0:
                break
            if no_results.count() > 0 and no_results.first.is_visible():
                break
            time.sleep(0.5)

        if no_results.count() > 0 and no_results.first.is_visible():
            pytest.fail(
                f"Contacts search for '{contact_search_term}' returned no results."
            )

        expect(contact_items.first).to_be_visible(timeout=10000)
        contact_count = contact_items.count()
        assert contact_count >= 1, (
            f"Expected contacts search for '{contact_search_term}' to return results."
        )

        search_lower = contact_search_term.lower()
        for index in range(contact_count):
            contact = contact_items.nth(index)
            name_locator = contact.locator(self.CONTACT_NAME_SELECTOR).first
            expect(name_locator).to_be_visible(timeout=10000)
            name = name_locator.inner_text().strip()
            assert search_lower in name.lower(), (
                f"Contact {index + 1} name '{name}' does not match search "
                f"term '{contact_search_term}'."
            )
            print(f"Contact {index + 1}: {name}", flush=True)

        print(
            f"Contacts search for '{contact_search_term}' returned "
            f"{contact_count} result(s).",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

    def _verify_contacts_tab_count_displayed(self, sidebar: Locator) -> None:
        contacts_header = sidebar.locator(self.CONTACTS_HEADER_SELECTOR)
        expect(contacts_header.locator("h3")).to_have_text(
            self.CONTACTS_TAB_NAME,
            timeout=15000,
        )

        count_label = contacts_header.locator("p").filter(
            has_text=self.CONTACTS_COUNT_TEXT_PATTERN
        )
        expect(count_label).to_be_visible(timeout=15000)
        count_text = count_label.inner_text().strip()
        print(f"Contacts tab count label: {count_text}", flush=True)

        match = re.search(r"Showing (\d+)", count_text, re.I)
        assert match, (
            f"Could not parse contact count from Contacts tab label '{count_text}'."
        )
        displayed_count = int(match.group(1))

        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() >= displayed_count:
                break
            time.sleep(0.5)

        expect(contact_items.first).to_be_visible(timeout=10000)
        assert contact_items.count() == displayed_count, (
            "Contacts tab count label does not match displayed contact results. "
            f"Label: {displayed_count}, displayed: {contact_items.count()}"
        )

        self.page.wait_for_timeout(3000)

    def scroll_contacts_tab_to_end(self, sidebar: Locator) -> None:
        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() > 0:
                break
            time.sleep(0.5)

        expect(contact_items.first).to_be_visible(timeout=15000)
        contact_count = contact_items.count()
        assert contact_count >= 1, (
            "Expected contacts before scrolling to the end of the Contacts tab."
        )

        scroll_before = self._read_contacts_scroll_metrics(sidebar)
        print(
            "Contacts tab scroll metrics before end scroll: "
            f"top={scroll_before['scrollTop']}, "
            f"height={scroll_before['scrollHeight']}, "
            f"viewport={scroll_before['clientHeight']}",
            flush=True,
        )

        if contact_count > 1:
            contact_items.last.scroll_into_view_if_needed(timeout=15000)

        self._scroll_contacts_container_to_end(sidebar)
        self.page.wait_for_timeout(1000)

        scroll_after = self._read_contacts_scroll_metrics(sidebar)
        print(
            "Contacts tab scroll metrics after end scroll: "
            f"top={scroll_after['scrollTop']}, "
            f"height={scroll_after['scrollHeight']}, "
            f"viewport={scroll_after['clientHeight']}",
            flush=True,
        )

    def _read_contacts_scroll_metrics(self, sidebar: Locator) -> dict[str, int]:
        for selector in self.CONTACTS_SCROLL_CONTAINER_SELECTORS:
            scroll_container = sidebar.locator(selector).first
            if scroll_container.count() == 0:
                                continue

            metrics = self._read_scroll_container_metrics(scroll_container)
            if metrics["scrollHeight"] > metrics["clientHeight"] + 1:
                return metrics

        return sidebar.locator(self.CONTACT_ITEM_SELECTOR).first.evaluate(
            """el => {
                let node = el.parentElement;
                while (node) {
                    if (node.scrollHeight > node.clientHeight + 1) {
                        return {
                            scrollTop: node.scrollTop,
                            scrollHeight: node.scrollHeight,
                            clientHeight: node.clientHeight,
                        };
                    }
                    node = node.parentElement;
                }
                return { scrollTop: 0, scrollHeight: 0, clientHeight: 0 };
            }"""
        )

    def _scroll_contacts_container_to_end(self, sidebar: Locator) -> None:
        for selector in self.CONTACTS_SCROLL_CONTAINER_SELECTORS:
            scroll_container = sidebar.locator(selector).first
            if scroll_container.count() == 0:
                continue

            metrics = self._read_scroll_container_metrics(scroll_container)
            if metrics["scrollHeight"] <= metrics["clientHeight"] + 1:
                continue

            scroll_container.evaluate("node => { node.scrollTop = node.scrollHeight; }")
            return

        sidebar.locator(self.CONTACT_ITEM_SELECTOR).first.evaluate(
            """el => {
                let node = el.parentElement;
                while (node) {
                    if (node.scrollHeight > node.clientHeight + 1) {
                        node.scrollTop = node.scrollHeight;
                        return;
                    }
                    node = node.parentElement;
                }
            }"""
        )

    def _verify_contacts_tab_load_more_visibility(
        self,
        sidebar: Locator,
        total_contacts: int,
    ) -> None:
        self.page.wait_for_timeout(3000)
        load_more_button = sidebar.locator(self.CONTACTS_LOAD_MORE_BUTTON_SELECTOR)

        if total_contacts > self.CONTACTS_PAGE_SIZE:
            if load_more_button.count() == 0:
                load_more_button = self._ensure_load_more_contacts_button_visible(
                    sidebar
                )
            else:
                load_more_button = load_more_button.first
                load_more_button.scroll_into_view_if_needed(timeout=5000)

            expect(load_more_button).to_be_visible(timeout=15000)
            print(
                f"{self.LOAD_MORE_CONTACTS_BUTTON_TEXT} button is visible for "
                f"{total_contacts} contacts.",
                flush=True,
            )
            return

        assert load_more_button.count() == 0, (
            f"{self.LOAD_MORE_CONTACTS_BUTTON_TEXT} button should not be displayed "
            f"when the General tab shows {total_contacts} contacts, but the button "
            "was found on the Contacts tab."
        )
        print(
            f"{self.LOAD_MORE_CONTACTS_BUTTON_TEXT} button is not displayed for "
            f"{total_contacts} contacts.",
            flush=True,
        )

    def _load_more_contacts_button(self, sidebar: Locator) -> Locator:
        role_based = sidebar.get_by_role(
            "button",
            name=re.compile(re.escape(self.LOAD_MORE_CONTACTS_BUTTON_TEXT), re.I),
        )
        if role_based.count() > 0:
            return role_based.first

        return sidebar.locator(self.CONTACTS_LOAD_MORE_BUTTON_SELECTOR).filter(
            has_text=re.compile(re.escape(self.LOAD_MORE_CONTACTS_BUTTON_TEXT), re.I)
        ).first

    def _ensure_load_more_contacts_button_visible(
        self,
        sidebar: Locator,
    ) -> Locator:
        load_more_button = self._load_more_contacts_button(sidebar)
        expect(load_more_button).to_be_attached(timeout=15000)

        if self._is_info_label_in_scroll_viewport(load_more_button):
            return load_more_button

        scroll_before = self._read_general_tab_scroll_metrics(load_more_button)
        print(
            "Contacts tab scroll before: "
            f"top={scroll_before['scrollTop']}, "
            f"height={scroll_before['scrollHeight']}, "
            f"viewport={scroll_before['clientHeight']}",
            flush=True,
        )

        for _ in range(60):
            if self._is_info_label_in_scroll_viewport(load_more_button):
                            break

            scrolled = self._scroll_info_label_toward_viewport(load_more_button)
            if not scrolled:
                self._wheel_scroll_contacts_tab_down(sidebar)
            self.page.wait_for_timeout(200)

        self.page.wait_for_timeout(3000)
        load_more_button.scroll_into_view_if_needed(timeout=5000)
        expect(load_more_button).to_be_visible(timeout=15000)
        assert self._is_info_label_in_scroll_viewport(load_more_button), (
            f"{self.LOAD_MORE_CONTACTS_BUTTON_TEXT} button is not visible "
            "in the Contacts tab viewport after scrolling."
        )

        scroll_after = self._read_general_tab_scroll_metrics(load_more_button)
        print(
            "Contacts tab scroll after: "
            f"top={scroll_after['scrollTop']}, "
            f"height={scroll_after['scrollHeight']}, "
            f"viewport={scroll_after['clientHeight']}",
            flush=True,
        )
        return load_more_button

    def _load_more_contacts(self, sidebar: Locator) -> None:
        contact_items = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        load_more_button = self._load_more_contacts_button(sidebar)
        expect(load_more_button).to_be_visible(timeout=10000)

        count_before = contact_items.count()
        assert count_before >= 1, (
            f"Expected contacts before {self.LOAD_MORE_CONTACTS_BUTTON_TEXT}."
        )
        print(
            f"Contact count before {self.LOAD_MORE_CONTACTS_BUTTON_TEXT}: "
            f"{count_before}",
            flush=True,
        )

        def api_matches(response) -> bool:
            return (
                Config.DAKOTA_SEARCH_API_URL in response.url
                and response.status == Config.DAKOTA_SEARCH_EXPECTED_API_STATUS
            )

        with self.page.expect_response(api_matches, timeout=30000) as response_info:
            load_more_button.click()

        response = response_info.value
        print(
            f"Load more contacts API responded with {response.status}: "
            f"{response.url}",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

        deadline = time.time() + 15
        while time.time() < deadline:
            if contact_items.count() > count_before:
                        break
                    time.sleep(0.5)

        count_after = contact_items.count()
        print(
            f"Contact count after {self.LOAD_MORE_CONTACTS_BUTTON_TEXT}: "
            f"{count_after}",
            flush=True,
        )
        assert count_after > count_before, (
            f'Expected more contacts after clicking "{self.LOAD_MORE_CONTACTS_BUTTON_TEXT}", '
            f"but count stayed at {count_after}."
        )
        expect(contact_items.nth(count_before)).to_be_visible(timeout=10000)

    def _wheel_scroll_contacts_tab_down(self, sidebar: Locator) -> None:
        for selector in self.CONTACTS_SCROLL_CONTAINER_SELECTORS:
            scroll_container = sidebar.locator(selector).first
            if scroll_container.count() == 0:
                continue

            metrics = self._read_scroll_container_metrics(scroll_container)
            if metrics["scrollHeight"] <= metrics["clientHeight"] + 1:
                continue

            scroll_container.hover(force=True, timeout=3000)
            self.page.mouse.wheel(0, 500)
            return

        sidebar.hover(force=True, timeout=3000)
        self.page.mouse.wheel(0, 500)

    def _open_investors_tab(self, sidebar: Locator) -> None:
        investors_tab = sidebar.locator(self.INVESTORS_TAB_SELECTOR).filter(
            has_text=re.compile(rf"^{re.escape(self.INVESTORS_TAB_NAME)}$")
        ).first
        expect(investors_tab).to_be_visible(timeout=10000)
        investors_tab.click()
        self.page.wait_for_timeout(3000)
        print(f"Navigated to {self.INVESTORS_TAB_NAME} tab.", flush=True)

    def _verify_investors_tab_content_displayed(self, sidebar: Locator) -> None:
        no_results = sidebar.locator(".dakota-no-results p").filter(
            has_text=re.compile(re.escape(self.INVESTORS_NO_RESULTS_TEXT), re.I)
        )
        investor_items = sidebar.locator(self.INVESTOR_ITEM_SELECTOR)

        expect(no_results.or_(investor_items.first)).to_be_visible(timeout=15000)

        if no_results.count() > 0 and no_results.first.is_visible():
            print(
                f"Investors tab displayed empty state: {self.INVESTORS_NO_RESULTS_TEXT}",
                flush=True,
            )
        else:
            expect(investor_items.first).to_be_visible(timeout=10000)
            investor_count = investor_items.count()
            print(
                f"Investors tab displayed {investor_count} investor result(s).",
                flush=True,
            )

        self.page.wait_for_timeout(3000)

    def _verify_investors_metro_areas_displayed(self, sidebar: Locator) -> None:
        investor_items = sidebar.locator(self.INVESTOR_ITEM_SELECTOR)
        expect(investor_items.first).to_be_visible(timeout=15000)

        investor_count = investor_items.count()
        assert investor_count >= 1, (
            "Expected at least one investor to verify state/city display."
        )

        for index in range(investor_count):
            investor = investor_items.nth(index)
            metro = investor.locator(self.INVESTOR_DETAILS_SELECTOR).locator(
                self.INVESTOR_METRO_SELECTOR
            ).first
            expect(metro).to_be_visible(timeout=10000)
            metro_text = metro.inner_text().strip()
            assert metro_text, (
                f"Investor {index + 1} of {investor_count} is missing a state/city."
            )
            print(
                f"Investor {index + 1} state/city: {metro_text}",
                flush=True,
            )

        print(
            f"All {investor_count} investor(s) display a state/city.",
            flush=True,
        )

    def _verify_investors_tab_count_displayed(self, sidebar: Locator) -> None:
        investors_header = sidebar.locator(self.INVESTORS_HEADER_SELECTOR)
        expect(investors_header.locator("h3")).to_have_text(
            self.INVESTORS_TAB_NAME,
            timeout=15000,
        )

        count_label = investors_header.locator("p").filter(
            has_text=self.INVESTORS_COUNT_TEXT_PATTERN
        )
        expect(count_label).to_be_visible(timeout=15000)
        count_text = count_label.inner_text().strip()
        print(f"Investors tab count label: {count_text}", flush=True)

        match = re.search(r"Showing (\d+)", count_text, re.I)
        assert match, (
            f"Could not parse investor count from Investors tab label '{count_text}'."
        )
        displayed_count = int(match.group(1))
        investor_items = sidebar.locator(self.INVESTOR_ITEM_SELECTOR)
        expect(investor_items.first).to_be_visible(timeout=10000)
        assert investor_items.count() == displayed_count, (
            "Investors tab count label does not match displayed investor results. "
            f"Label: {displayed_count}, displayed: {investor_items.count()}"
        )

    def _load_more_investors_button(self, sidebar: Locator) -> Locator:
        role_based = sidebar.get_by_role(
            "button",
            name=re.compile(re.escape(self.LOAD_MORE_INVESTORS_BUTTON_TEXT), re.I),
        )
        if role_based.count() > 0:
            return role_based.first

        return sidebar.locator("button.dakota-load-more-button").filter(
            has_text=re.compile(re.escape(self.LOAD_MORE_INVESTORS_BUTTON_TEXT), re.I)
        ).first

    def _ensure_load_more_investors_button_visible(
        self,
        sidebar: Locator,
    ) -> Locator:
        load_more_button = self._load_more_investors_button(sidebar)
        expect(load_more_button).to_be_attached(timeout=15000)

        if self._is_info_label_in_scroll_viewport(load_more_button):
            return load_more_button

        scroll_before = self._read_general_tab_scroll_metrics(load_more_button)
        print(
            "Investors tab scroll before: "
            f"top={scroll_before['scrollTop']}, "
            f"height={scroll_before['scrollHeight']}, "
            f"viewport={scroll_before['clientHeight']}",
            flush=True,
        )

        for _ in range(60):
            if self._is_info_label_in_scroll_viewport(load_more_button):
                break

            scrolled = self._scroll_info_label_toward_viewport(load_more_button)
            if not scrolled:
                self._wheel_scroll_investors_tab_down(sidebar)
            self.page.wait_for_timeout(200)

        self.page.wait_for_timeout(3000)
        load_more_button.scroll_into_view_if_needed(timeout=5000)
        expect(load_more_button).to_be_visible(timeout=15000)
        assert self._is_info_label_in_scroll_viewport(load_more_button), (
            f"{self.LOAD_MORE_INVESTORS_BUTTON_TEXT} button is not visible "
            "in the Investors tab viewport after scrolling."
        )

        scroll_after = self._read_general_tab_scroll_metrics(load_more_button)
        print(
            "Investors tab scroll after: "
            f"top={scroll_after['scrollTop']}, "
            f"height={scroll_after['scrollHeight']}, "
            f"viewport={scroll_after['clientHeight']}",
            flush=True,
        )
        return load_more_button

    def _load_more_investors(self, sidebar: Locator) -> None:
        investor_items = sidebar.locator(self.INVESTOR_ITEM_SELECTOR)
        load_more_button = self._load_more_investors_button(sidebar)
        expect(load_more_button).to_be_visible(timeout=10000)

        count_before = investor_items.count()
        assert count_before >= 1, (
            f"Expected investors before {self.LOAD_MORE_INVESTORS_BUTTON_TEXT}."
        )
        print(
            f"Investor count before {self.LOAD_MORE_INVESTORS_BUTTON_TEXT}: "
            f"{count_before}",
            flush=True,
        )

        def api_matches(response) -> bool:
            return (
                Config.DAKOTA_SEARCH_API_URL in response.url
                and response.status == Config.DAKOTA_SEARCH_EXPECTED_API_STATUS
            )

        with self.page.expect_response(api_matches, timeout=30000) as response_info:
            load_more_button.click()

        response = response_info.value
        print(
            f"Load more investors API responded with {response.status}: "
            f"{response.url}",
            flush=True,
        )
        self.page.wait_for_timeout(3000)

        deadline = time.time() + 15
        while time.time() < deadline:
            if investor_items.count() > count_before:
                break
            time.sleep(0.5)

        count_after = investor_items.count()
        print(
            f"Investor count after {self.LOAD_MORE_INVESTORS_BUTTON_TEXT}: "
            f"{count_after}",
            flush=True,
        )
        assert count_after > count_before, (
            f'Expected more investors after clicking "{self.LOAD_MORE_INVESTORS_BUTTON_TEXT}", '
            f"but count stayed at {count_after}."
        )
        expect(investor_items.nth(count_before)).to_be_visible(timeout=10000)

    def scroll_investors_tab_to_end(self, sidebar: Locator) -> None:
        investor_items = sidebar.locator(self.INVESTOR_ITEM_SELECTOR)
        expect(investor_items.first).to_be_visible(timeout=15000)

        investor_count = investor_items.count()
        assert investor_count >= 1, (
            "Expected investors before scrolling to the end of the Investors tab."
        )

        scroll_before = self._read_investors_scroll_metrics(sidebar)
        print(
            "Investors tab scroll metrics before end scroll: "
            f"top={scroll_before['scrollTop']}, "
            f"height={scroll_before['scrollHeight']}, "
            f"viewport={scroll_before['clientHeight']}",
            flush=True,
        )

        if investor_count > 1:
            investor_items.last.scroll_into_view_if_needed(timeout=15000)

        self._scroll_investors_container_to_end(sidebar)
        self.page.wait_for_timeout(1000)

        scroll_after = self._read_investors_scroll_metrics(sidebar)
        print(
            "Investors tab scroll metrics after end scroll: "
            f"top={scroll_after['scrollTop']}, "
            f"height={scroll_after['scrollHeight']}, "
            f"viewport={scroll_after['clientHeight']}",
            flush=True,
        )

        self._verify_investors_scrolled_to_end(scroll_before, scroll_after)
        if investor_count > 1:
            expect(investor_items.last).to_be_in_viewport(timeout=5000)

    def _read_investors_scroll_metrics(self, sidebar: Locator) -> dict[str, int]:
        investors_page = sidebar.locator(self.INVESTORS_PAGE_SELECTOR).first
        if investors_page.count() > 0:
            return self._read_scroll_container_metrics(investors_page)

        return sidebar.locator(self.INVESTOR_ITEM_SELECTOR).first.evaluate(
            """el => {
                let node = el.parentElement;
                while (node) {
                    if (node.scrollHeight > node.clientHeight + 1) {
                        return {
                            scrollTop: node.scrollTop,
                            scrollHeight: node.scrollHeight,
                            clientHeight: node.clientHeight,
                        };
                    }
                    node = node.parentElement;
                }
                return { scrollTop: 0, scrollHeight: 0, clientHeight: 0 };
            }"""
        )

    def _scroll_investors_container_to_end(self, sidebar: Locator) -> None:
        investors_page = sidebar.locator(self.INVESTORS_PAGE_SELECTOR).first
        if investors_page.count() > 0:
            investors_page.evaluate("node => { node.scrollTop = node.scrollHeight; }")
            return

        sidebar.locator(self.INVESTOR_ITEM_SELECTOR).first.evaluate(
            """el => {
                let node = el.parentElement;
                while (node) {
                    if (node.scrollHeight > node.clientHeight + 1) {
                        node.scrollTop = node.scrollHeight;
                        return;
                    }
                    node = node.parentElement;
                }
            }"""
        )

    def _verify_investors_scrolled_to_end(
        self,
        scroll_before: dict[str, int],
        scroll_after: dict[str, int],
    ) -> None:
        scroll_height = scroll_after["scrollHeight"]
        client_height = scroll_after["clientHeight"]
        scroll_top = scroll_after["scrollTop"]

        if scroll_height <= client_height + 1:
            print(
                "Investors tab list is not scrollable; already fully visible.",
                flush=True,
            )
            return

        at_bottom = scroll_top + client_height >= scroll_height - 2
        if not at_bottom:
                    pytest.fail(
                "Investors tab did not scroll to the end. "
                f"scrollTop={scroll_top}, clientHeight={client_height}, "
                f"scrollHeight={scroll_height}"
            )

        if scroll_top < scroll_before["scrollTop"]:
            pytest.fail(
                "Investors tab scroll position moved upward unexpectedly. "
                f"before={scroll_before['scrollTop']}, after={scroll_top}"
            )

        print(
            "Investors tab scrolled successfully to the end of the list.",
            flush=True,
        )

    def _wheel_scroll_investors_tab_down(self, sidebar: Locator) -> None:
        for selector in self.INVESTORS_SCROLL_CONTAINER_SELECTORS:
            scroll_container = sidebar.locator(selector).first
            if scroll_container.count() == 0:
                continue

            metrics = self._read_scroll_container_metrics(scroll_container)
            if metrics["scrollHeight"] <= metrics["clientHeight"] + 1:
                continue

            scroll_container.hover(force=True, timeout=3000)
            self.page.mouse.wheel(0, 500)
            return

        sidebar.hover(force=True, timeout=3000)
        self.page.mouse.wheel(0, 500)

    def _open_investment_details_tab(self, sidebar: Locator) -> None:
        investment_details_tab = sidebar.locator(
            self.INVESTMENT_DETAILS_TAB_SELECTOR
        ).filter(
            has_text=re.compile(r"^Investment\s+Details$", re.I)
        ).first
        expect(investment_details_tab).to_be_visible(timeout=10000)
        investment_details_tab.click()
        self.page.wait_for_timeout(3000)
        print(
            f"Navigated to {self.INVESTMENT_DETAILS_TAB_NAME} tab.",
            flush=True,
        )

    def _verify_investment_details_tab_content_displayed(
        self,
        sidebar: Locator,
    ) -> None:
        no_content = sidebar.locator(".dakota-no-content p").filter(
            has_text=re.compile(
                rf"{re.escape(self.INVESTMENT_DETAILS_NO_CONTENT_TEXT)}\.?",
                re.I,
            )
        )
        detail_items = sidebar.locator(self.INVESTMENT_DETAILS_ITEM_SELECTOR)

        expect(no_content.or_(detail_items.first)).to_be_visible(timeout=15000)

        if no_content.count() > 0 and no_content.first.is_visible():
            print(
                "Investment Details tab displayed empty state: "
                f"{self.INVESTMENT_DETAILS_NO_CONTENT_TEXT}",
                flush=True,
            )
        else:
            expect(detail_items.first).to_be_visible(timeout=10000)
            detail_count = detail_items.count()
            print(
                f"Investment Details tab displayed {detail_count} detail item(s).",
                flush=True,
            )

        self.page.wait_for_timeout(3000)

    def _verify_investment_details_geography_displayed(
        self,
        sidebar: Locator,
    ) -> None:
        geography_item = sidebar.locator(
            f"{self.INVESTMENT_DETAILS_ITEM_SELECTOR}:has("
            f"h3:text-is('{self.INVESTMENT_DETAILS_GEOGRAPHY_LABEL}'))"
        ).first
        expect(geography_item).to_be_visible(timeout=15000)
        expect(geography_item.locator("h3")).to_have_text(
            self.INVESTMENT_DETAILS_GEOGRAPHY_LABEL,
            timeout=10000,
        )

        geography_value = geography_item.locator(
            self.INVESTMENT_DETAILS_DESCRIPTION_SELECTOR
        ).first
        expect(geography_value).to_be_visible(timeout=10000)
        geography_text = geography_value.inner_text().strip()
        assert geography_text, (
            f"Expected a displayed {self.INVESTMENT_DETAILS_GEOGRAPHY_LABEL} value "
            "on the Investment Details tab."
        )
        print(
            f"Investment Details {self.INVESTMENT_DETAILS_GEOGRAPHY_LABEL}: "
            f"{geography_text}",
            flush=True,
        )

        self.page.wait_for_timeout(3000)

    def _verify_investment_details_industry_displayed(
        self,
        sidebar: Locator,
    ) -> None:
        industry_item = sidebar.locator(
            f"{self.INVESTMENT_DETAILS_ITEM_SELECTOR}:has("
            f"h3:text-is('{self.INVESTMENT_DETAILS_INDUSTRY_LABEL}'))"
        ).first
        expect(industry_item).to_be_visible(timeout=15000)
        expect(industry_item.locator("h3")).to_have_text(
            self.INVESTMENT_DETAILS_INDUSTRY_LABEL,
            timeout=10000,
        )

        industry_value = industry_item.locator(
            self.INVESTMENT_DETAILS_DESCRIPTION_SELECTOR
        ).first
        expect(industry_value).to_be_visible(timeout=10000)
        industry_text = industry_value.inner_text().strip()
        assert industry_text, (
            f"Expected a displayed {self.INVESTMENT_DETAILS_INDUSTRY_LABEL} value "
            "on the Investment Details tab."
        )
        print(
            f"Investment Details {self.INVESTMENT_DETAILS_INDUSTRY_LABEL}: "
            f"{industry_text}",
            flush=True,
        )

        self.page.wait_for_timeout(3000)

    def _verify_investment_details_check_size_displayed(
        self,
        sidebar: Locator,
    ) -> None:
        check_size_item = sidebar.locator(
            f"{self.INVESTMENT_DETAILS_ITEM_SELECTOR}:has("
            f"h3:text-is('{self.INVESTMENT_DETAILS_CHECK_SIZE_LABEL}'))"
        ).first
        expect(check_size_item).to_be_visible(timeout=15000)
        expect(check_size_item.locator("h3")).to_have_text(
            self.INVESTMENT_DETAILS_CHECK_SIZE_LABEL,
            timeout=10000,
        )

        check_size_value = check_size_item.locator(
            self.INVESTMENT_DETAILS_DESCRIPTION_SELECTOR
        ).first
        expect(check_size_value).to_be_visible(timeout=10000)
        check_size_text = check_size_value.inner_text().strip()
        assert check_size_text, (
            f"Expected a displayed {self.INVESTMENT_DETAILS_CHECK_SIZE_LABEL} value "
            "on the Investment Details tab."
        )
        print(
            f"Investment Details {self.INVESTMENT_DETAILS_CHECK_SIZE_LABEL}: "
            f"{check_size_text}",
            flush=True,
        )

        self.page.wait_for_timeout(3000)

    def _open_platform_details_tab(self, sidebar: Locator) -> None:
        platform_details_tab = sidebar.locator(
            self.PLATFORM_DETAILS_TAB_SELECTOR
        ).filter(
            has_text=re.compile(r"^Platform\s+Details$", re.I)
        ).first
        expect(platform_details_tab).to_be_visible(timeout=10000)
        platform_details_tab.click()
        self.page.wait_for_timeout(3000)
        print(
            f"Navigated to {self.PLATFORM_DETAILS_TAB_NAME} tab.",
            flush=True,
        )

    def _verify_platform_details_platform_description_displayed(
        self,
        sidebar: Locator,
    ) -> None:
        platform_description_item = sidebar.locator(
            f"{self.PLATFORM_DETAILS_ITEM_SELECTOR}:has("
            f"h3:text-is('{self.PLATFORM_DETAILS_PLATFORM_DESCRIPTION_LABEL}'))"
        ).first
        expect(platform_description_item).to_be_visible(timeout=15000)
        expect(platform_description_item.locator("h3")).to_have_text(
            self.PLATFORM_DETAILS_PLATFORM_DESCRIPTION_LABEL,
            timeout=10000,
        )

        description_value = platform_description_item.locator(
            self.PLATFORM_DETAILS_DESCRIPTION_SELECTOR
        ).first
        expect(description_value).to_be_visible(timeout=10000)
        description_text = description_value.inner_text().strip()
        assert description_text, (
            "Expected a displayed Platform Description value "
            "on the Platform Details tab."
        )
        print(
            f"Platform Details {self.PLATFORM_DETAILS_PLATFORM_DESCRIPTION_LABEL}: "
            f"{description_text}",
            flush=True,
        )

        self.page.wait_for_timeout(3000)

    def _count_contacts_on_contacts_tab(self, sidebar: Locator) -> int:
        contacts = sidebar.locator(self.CONTACT_ITEM_SELECTOR)
        deadline = time.time() + 15
        while time.time() < deadline:
            count = contacts.count()
            if count > 0:
                expect(contacts.first).to_be_visible(timeout=5000)
                return count
            time.sleep(0.5)

        return 0

    def _verify_company_details_content_displayed(
        self,
        sidebar: Locator,
        search_term: str,
    ) -> None:
        expect(sidebar).to_be_visible(timeout=5000)

        deadline = time.time() + 15
        while time.time() < deadline:
            visible_text = sidebar.inner_text().strip()
            if len(visible_text) >= 30:
                print(
                    f"Company details content displayed after searching "
                    f"'{search_term}' ({len(visible_text)} characters)",
                    flush=True,
                )
                return
            time.sleep(0.5)

        pytest.fail(
            "No company details content was displayed in the sidebar after "
            f"opening a search result for '{search_term}'."
        )

    def _read_results_scroll_metrics(self, sidebar: Locator) -> dict[str, int]:
        return sidebar.locator(self.SEARCH_RESULT_ITEM_SELECTOR).first.evaluate(
            """el => {
                let node = el.parentElement;
                while (node) {
                    if (node.scrollHeight > node.clientHeight + 1) {
                        return {
                            scrollTop: node.scrollTop,
                            scrollHeight: node.scrollHeight,
                            clientHeight: node.clientHeight,
                        };
                    }
                    node = node.parentElement;
                }
                return { scrollTop: 0, scrollHeight: 0, clientHeight: 0 };
            }"""
        )

    def _scroll_results_container_to_end(self, sidebar: Locator) -> None:
        sidebar.locator(self.SEARCH_RESULT_ITEM_SELECTOR).first.evaluate(
            """el => {
                let node = el.parentElement;
                while (node) {
                    if (node.scrollHeight > node.clientHeight + 1) {
                        node.scrollTop = node.scrollHeight;
                        return;
                    }
                    node = node.parentElement;
                }
            }"""
        )

    def _verify_results_scrolled_to_end(
        self,
        scroll_before: dict[str, int],
        scroll_after: dict[str, int],
    ) -> None:
        scroll_height = scroll_after["scrollHeight"]
        client_height = scroll_after["clientHeight"]
        scroll_top = scroll_after["scrollTop"]

        if scroll_height <= client_height + 1:
            print("Results list is not scrollable; already fully visible.")
            return

        at_bottom = scroll_top + client_height >= scroll_height - 2
        if not at_bottom:
            pytest.fail(
                "Search results did not scroll to the end. "
                f"scrollTop={scroll_top}, clientHeight={client_height}, "
                f"scrollHeight={scroll_height}"
            )

        if scroll_top < scroll_before["scrollTop"]:
            pytest.fail(
                "Search results scroll position moved upward unexpectedly. "
                f"before={scroll_before['scrollTop']}, after={scroll_top}"
            )

        print("Search results scrolled successfully to the end of the list.")

    def _ensure_browser_window_focused(self) -> None:
        self.page.bring_to_front()
        dismiss_marketplace_obstructions(self.page)
        self.page.mouse.click(120, 120)
        time.sleep(0.5)

    def open_from_extension_toolbar(self) -> None:
        """Click the pinned Dakota icon and require the sidebar panel to open."""
        self._ensure_browser_window_focused()

        if not self.is_sidebar_open():
            icon_position = Config.CHROME_DAKOTA_EXTENSION_ICON_POSITION
            print(f"Clicking Dakota extension icon at {icon_position}")
            native_left_click(icon_position)
        time.sleep(1)

        if not self.is_sidebar_open():
            print("Toolbar click did not open sidebar; trying in-page floating button.")
            self.open_sidebar_if_closed()

        try:
            expect(self._sidebar()).to_be_visible(timeout=15000)
        except (AssertionError, PlaywrightTimeoutError):
            screen_width, screen_height = pyautogui.size()
            icon_position = Config.CHROME_DAKOTA_EXTENSION_ICON_POSITION
            pytest.fail(
                "Dakota sidebar did not open after clicking the extension toolbar icon. "
                f"Clicked at {icon_position} on a {screen_width}x{screen_height} display. "
                "Update CHROME_DAKOTA_EXTENSION_ICON_X/Y in config or env vars."
            )

        self.page.wait_for_timeout(1000)

    def _sidebar(self) -> Locator:
        return self.page.locator(self.SIDEBAR_OPEN_SELECTOR).first

    def _snapshot_open_pages(self) -> set[Page]:
        return set(self.page.context.pages)

    def _is_salesforce_login_page(self, candidate: Page) -> bool:
        try:
            url = candidate.url.lower()
            title = candidate.title().lower()
        except Exception:
            return False
        return (
            "salesforce.com" in url
            or "login" in title
            or "salesforce" in title
        )

    def _dismiss_premature_salesforce_tabs(self, pages_before_navigation: set[Page]) -> None:
        """Close auth tabs that open on page load before the sidebar flow runs."""
        for candidate in list(self.page.context.pages):
            if candidate in pages_before_navigation or candidate == self.page:
                continue
            if self._is_salesforce_login_page(candidate):
                print(
                    "Closing premature Salesforce tab opened before sidebar flow: "
                    f"{candidate.url}"
                )
                candidate.close()

    def _wait_for_sidebar_auth_state(self, timeout_s: float = 30) -> bool:
        """Return True when logged in (search visible), False when login is required."""
        sidebar = self._sidebar()
        expect(sidebar).to_be_visible(timeout=5000)

        deadline = time.time() + timeout_s
        while time.time() < deadline:
            if sidebar.locator(self.SEARCH_BAR_SELECTOR).first.is_visible(timeout=200):
                print("Session detected: search bar visible in open sidebar.")
                return True
            if sidebar.locator(self.LOGIN_BUTTON_SELECTOR).first.is_visible(timeout=200):
                print("No session detected: Login to Dakota button visible in open sidebar.")
                return False
            time.sleep(0.5)

        pytest.fail(
            "Open sidebar did not show either the search bar (logged in) or "
            "the Login to Dakota button within 30s."
        )

    def _wait_for_salesforce_login_page(self, timeout_s: float = 30) -> Page:
        login_page = None
        for attempt in range(int(timeout_s * 2)):
            for candidate in self.page.context.pages:
                if candidate == self.page:
                    continue
                if self._is_salesforce_login_page(candidate):
                    login_page = candidate
                    print(f"Found Salesforce login page: {candidate.url}")
                    break
            if login_page:
                break
            if attempt % 10 == 0:
                print("Waiting for Salesforce login tab after sidebar login click...")
            time.sleep(0.5)

        if not login_page:
            pytest.fail(
                "Salesforce login page not found after clicking Login to Dakota in the sidebar."
            )
        return login_page

    def is_sidebar_open(self) -> bool:
        return self._sidebar().is_visible(timeout=200)

    def _verify_search_results_visible(self, search_term: str) -> None:
        sidebar = self._sidebar()
        expect(sidebar).to_be_visible(timeout=5000)

        results = sidebar.locator(self.SEARCH_RESULT_ITEM_SELECTOR)
        expect(results.first).to_be_visible(timeout=15000)
        assert results.count() >= 1, (
            f"Expected at least one search result for '{search_term}', got 0."
        )
        expect(results.first.locator(self.SEARCH_RESULT_NAME_SELECTOR)).to_be_visible()
        self.page.wait_for_timeout(3000)

    def find_search_bar(self) -> Locator | None:
        if not self.is_sidebar_open():
            return None

        sidebar = self._sidebar()
        for selector in self.SEARCH_BAR_SELECTORS:
            try:
                locator = sidebar.locator(selector).first
                if locator.is_visible(timeout=200):
                    return locator
            except Exception:
                continue
        return None

    def open_sidebar_if_closed(self) -> None:
        if self.is_sidebar_open():
            return

        toggle = self.page.locator(self.SIDEBAR_TOGGLE_SELECTOR).first
        if toggle.is_visible(timeout=2000):
            toggle.evaluate("el => el.click()")
            self.page.wait_for_timeout(500)

        deadline = time.time() + 10
        while time.time() < deadline:
            if self.is_sidebar_open():
                return
            time.sleep(0.25)

    def ensure_sidebar_ready(self, timeout_s: float = 30) -> Locator:
        deadline = time.time() + timeout_s
        while time.time() < deadline:
            search_bar = self.find_search_bar()
            if search_bar:
                return search_bar

            self.open_sidebar_if_closed()
            time.sleep(0.5)

        print("DEBUG: Search bar not found. Listing all available inputs:")
        try:
            for index, input_field in enumerate(self.page.locator("input").all()):
                print(
                    f"  Input {index}: id='{input_field.get_attribute('id')}', "
                    f"name='{input_field.get_attribute('name')}', "
                    f"visible={input_field.is_visible()}"
                )
        except Exception:
            pass

        pytest.fail("Could not find the search bar in the Dakota sidebar.")

    def wait_for_salesforce_auth(self, login_page: Page, timeout_ms: int = 60000) -> None:
        try:
            login_page.wait_for_event("close", timeout=timeout_ms)
        except Exception:
            login_page.wait_for_load_state("networkidle", timeout=timeout_ms)

        self.page.bring_to_front()
        self.page.wait_for_timeout(1500)

    def _replace_input_value(self, field: Locator, value: str) -> None:
        field.click()
        field.press("Control+A")
        field.press("Backspace")
        field.fill(value)

    def submit_salesforce_login(
        self,
        login_page: Page,
        username: str,
        password: str,
    ) -> None:
        login_page.bring_to_front()
        login_page.wait_for_load_state("load", timeout=30000)

        username_selectors = (
            "#username",
            "input[name='username']",
            "input[type='email']",
            "input[placeholder*='Username']",
        )

        username_field = None
        for selector in username_selectors:
            try:
                locator = login_page.locator(selector).first
                if locator.is_visible(timeout=2000):
                    username_field = locator
                    break
            except Exception:
                continue

        if not username_field:
            username_field = login_page.locator("#username").first
            username_field.wait_for(state="visible", timeout=30000)

        self._replace_input_value(username_field, username)

        password_field = login_page.locator(
            "input[type='password'], #password"
        ).filter(visible=True).first
        self._replace_input_value(password_field, password)

        login_btn = login_page.locator(
            "#Login, #login_button, input[type='submit']"
        ).filter(visible=True).first
        login_btn.click()
