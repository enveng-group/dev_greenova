"""Global constants and choices for Greenova.

This module centralizes status, role, and frequency constants for use across all apps.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Final

# Status choices for obligations and similar models
STATUS_NOT_STARTED = "not started"
STATUS_IN_PROGRESS = "in progress"
STATUS_COMPLETED = "completed"
STATUS_OVERDUE = "overdue"
STATUS_UPCOMING = "upcoming"

STATUS_CHOICES: list[tuple[str, str]] = [
    (STATUS_NOT_STARTED, "Not Started"),
    (STATUS_IN_PROGRESS, "In Progress"),
    (STATUS_COMPLETED, "Completed"),
]

# Obligation status choices for use in obligations app
OBLIGATION_STATUS_CHOICES: list[tuple[str, str]] = [
    (STATUS_NOT_STARTED, "Not Started"),
    (STATUS_IN_PROGRESS, "In Progress"),
    (STATUS_COMPLETED, "Completed"),
    (STATUS_OVERDUE, "Overdue"),
]

# Due date periods for filtering
DUE_PERIOD_OVERDUE = "overdue"
DUE_PERIOD_THIS_WEEK = "this_week"
DUE_PERIOD_NEXT_WEEK = "next_week"
DUE_PERIOD_THIS_MONTH = "this_month"
DUE_PERIOD_NEXT_MONTH = "next_month"

# Recurring frequency constants
FREQUENCY_DAILY = "daily"
FREQUENCY_WEEKLY = "weekly"
FREQUENCY_FORTNIGHTLY = "fortnightly"
FREQUENCY_MONTHLY = "monthly"
FREQUENCY_QUARTERLY = "quarterly"
FREQUENCY_BIANNUAL = "biannual"
FREQUENCY_ANNUAL = "annual"

# Alternative terms that should be normalized
FREQUENCY_SEMI_ANNUAL = "semi-annual"  # should be treated as biannual
FREQUENCY_BI_ANNUALLY = "bi-annually"  # should be treated as biannual
FREQUENCY_YEARLY = "yearly"  # should be treated as annual
FREQUENCY_ANNUALLY = "annually"  # should be treated as annual

# Display names for frequencies (for UI)
FREQUENCY_DISPLAY_NAMES = {
    FREQUENCY_DAILY: "Daily",
    FREQUENCY_WEEKLY: "Weekly",
    FREQUENCY_FORTNIGHTLY: "Fortnightly",
    FREQUENCY_MONTHLY: "Monthly",
    FREQUENCY_QUARTERLY: "Quarterly",
    FREQUENCY_BIANNUAL: "Bi-annual (Twice a year)",
    FREQUENCY_ANNUAL: "Annual (Once a year)",
}

# Choices for forms and models
FREQUENCY_CHOICES: list[tuple[str, str]] = [
    (FREQUENCY_DAILY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_DAILY]),
    (FREQUENCY_WEEKLY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_WEEKLY]),
    (FREQUENCY_FORTNIGHTLY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_FORTNIGHTLY]),
    (FREQUENCY_MONTHLY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_MONTHLY]),
    (FREQUENCY_QUARTERLY, FREQUENCY_DISPLAY_NAMES[FREQUENCY_QUARTERLY]),
    (FREQUENCY_BIANNUAL, FREQUENCY_DISPLAY_NAMES[FREQUENCY_BIANNUAL]),
    (FREQUENCY_ANNUAL, FREQUENCY_DISPLAY_NAMES[FREQUENCY_ANNUAL]),
]

# Mapping of alternative terms to canonical constants
FREQUENCY_ALIASES = {
    FREQUENCY_SEMI_ANNUAL: FREQUENCY_BIANNUAL,
    FREQUENCY_BI_ANNUALLY: FREQUENCY_BIANNUAL,
    FREQUENCY_YEARLY: FREQUENCY_ANNUAL,
    FREQUENCY_ANNUALLY: FREQUENCY_ANNUAL,
}

# Frequency duration in days (approximate)
FREQUENCY_DAYS = {
    FREQUENCY_DAILY: 1,
    FREQUENCY_WEEKLY: 7,
    FREQUENCY_FORTNIGHTLY: 14,
    FREQUENCY_MONTHLY: 30,  # Approximate
    FREQUENCY_QUARTERLY: 90,  # Approximate
    FREQUENCY_BIANNUAL: 182,  # Approximate
    FREQUENCY_ANNUAL: 365,  # Approximate
}

# Project role constants
ROLE_OWNER = "owner"
ROLE_MANAGER = "manager"
ROLE_MEMBER = "member"
ROLE_VIEWER = "viewer"

ROLE_CHOICES: list[tuple[str, str]] = [
    (ROLE_OWNER, "Owner"),
    (ROLE_MANAGER, "Manager"),
    (ROLE_MEMBER, "Member"),
    (ROLE_VIEWER, "Viewer"),
]

# Mechanism status color mapping (migrated from mechanisms/commons.py)
MECHANISM_STATUS_COLORS: dict[str, str] = {
    "Active": "#43aa8b",
    "Inactive": "#f9c74f",
    "Archived": "#b0b0b0",
}

# Mechanism types, categories, and operational modes (migrated from
# mechanisms/constants.py)
MECHANISM_TYPE_PHYSICAL: Final[str] = "physical"
MECHANISM_TYPE_CHEMICAL: Final[str] = "chemical"
MECHANISM_TYPE_BIOLOGICAL: Final[str] = "biological"
MECHANISM_TYPE_OTHER: Final[str] = "other"
MECHANISM_TYPE_CHOICES: Final[list[tuple[str, str]]] = [
    (MECHANISM_TYPE_PHYSICAL, "Physical"),
    (MECHANISM_TYPE_CHEMICAL, "Chemical"),
    (MECHANISM_TYPE_BIOLOGICAL, "Biological"),
    (MECHANISM_TYPE_OTHER, "Other"),
]

MECHANISM_CATEGORY_PREVENTION: Final[str] = "prevention"
MECHANISM_CATEGORY_CONTROL: Final[str] = "control"
MECHANISM_CATEGORY_MITIGATION: Final[str] = "mitigation"
MECHANISM_CATEGORY_CHOICES: Final[list[tuple[str, str]]] = [
    (MECHANISM_CATEGORY_PREVENTION, "Prevention"),
    (MECHANISM_CATEGORY_CONTROL, "Control"),
    (MECHANISM_CATEGORY_MITIGATION, "Mitigation"),
]

OPERATIONAL_MODE_AUTOMATIC: Final[str] = "automatic"
OPERATIONAL_MODE_MANUAL: Final[str] = "manual"
OPERATIONAL_MODE_CHOICES: Final[list[tuple[str, str]]] = [
    (OPERATIONAL_MODE_AUTOMATIC, "Automatic"),
    (OPERATIONAL_MODE_MANUAL, "Manual"),
]
