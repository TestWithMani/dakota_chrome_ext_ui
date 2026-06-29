"""Company type -> profile tab mapping (from Dakota_Ext_Performance)."""

ACCOUNT_CRITERIA_TO_PROFILE_TAB = {
    "allocator": "Platform Details",
    "firm": "Investment Details",
    "private": "Investors",
    "private company": "Investors",
    "public": "Earnings Events",
    "public company": "Earnings Events",
}


def profile_tab_for_company_type(company_type: str) -> str | None:
    normalized = company_type.strip().casefold()
    if normalized in ACCOUNT_CRITERIA_TO_PROFILE_TAB:
        return ACCOUNT_CRITERIA_TO_PROFILE_TAB[normalized]
    for key, tab in ACCOUNT_CRITERIA_TO_PROFILE_TAB.items():
        if key in normalized:
            return tab
    return None
