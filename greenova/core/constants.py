"""Global constants and choices for Greenova.

This module centralizes status, role, and frequency constants for use across all apps.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Final

# Status choices for obligations and similar models
STATUS_NOT_STARTED: Final[str] = "not started"
STATUS_IN_PROGRESS: Final[str] = "in progress"
STATUS_COMPLETED: Final[str] = "completed"
STATUS_OVERDUE: Final[str] = "overdue"
STATUS_UPCOMING: Final[str] = "upcoming"

STATUS_CHOICES: Final[list[tuple[str, str]]] = [
    (STATUS_NOT_STARTED, "Not Started"),
    (STATUS_IN_PROGRESS, "In Progress"),
    (STATUS_COMPLETED, "Completed"),
    (STATUS_OVERDUE, "Overdue"),
    (STATUS_UPCOMING, "Upcoming"),
]

OBLIGATION_STATUS_CHOICES: Final[list[tuple[str, str]]] = STATUS_CHOICES

# Due period constants
DUE_PERIOD_OVERDUE: Final[str] = "overdue"
DUE_PERIOD_THIS_WEEK: Final[str] = "this_week"
DUE_PERIOD_NEXT_WEEK: Final[str] = "next_week"
DUE_PERIOD_THIS_MONTH: Final[str] = "this_month"
DUE_PERIOD_NEXT_MONTH: Final[str] = "next_month"

# Frequency constants
FREQUENCY_DAILY: Final[str] = "daily"
FREQUENCY_WEEKLY: Final[str] = "weekly"
FREQUENCY_MONTHLY: Final[str] = "monthly"
FREQUENCY_QUARTERLY: Final[str] = "quarterly"
FREQUENCY_ANNUALLY: Final[str] = "annually"

FREQUENCY_CHOICES: Final[list[tuple[str, str]]] = [
    (FREQUENCY_DAILY, "Daily"),
    (FREQUENCY_WEEKLY, "Weekly"),
    (FREQUENCY_MONTHLY, "Monthly"),
    (FREQUENCY_QUARTERLY, "Quarterly"),
    (FREQUENCY_ANNUALLY, "Annually"),
]
