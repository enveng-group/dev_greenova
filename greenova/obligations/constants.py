"""Constants for the obligations app.

Defines static values and choices for obligation models and logic.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>

License:
    AGPL-3.0
"""

from core.constants import (
    STATUS_COMPLETED,
    STATUS_IN_PROGRESS,
    STATUS_NOT_STARTED,
    STATUS_OVERDUE,
)

OBLIGATION_DEFAULT_STATUS = "not started"

OBLIGATION_STATUS_CHOICES = [
    (STATUS_NOT_STARTED, "Not Started"),
    (STATUS_IN_PROGRESS, "In Progress"),
    (STATUS_COMPLETED, "Completed"),
    (STATUS_OVERDUE, "Overdue"),
]

FREQUENCY_DAILY = "Daily"
FREQUENCY_WEEKLY = "Weekly"
FREQUENCY_FORTNIGHTLY = "Fortnightly"
FREQUENCY_MONTHLY = "Monthly"
FREQUENCY_QUARTERLY = "Quarterly"
FREQUENCY_BIANNUAL = "Bi-Annually"
FREQUENCY_ANNUAL = "Annually"

FREQUENCY_ALIASES = {
    "day": FREQUENCY_DAILY,
    "week": FREQUENCY_WEEKLY,
    "fortnight": FREQUENCY_FORTNIGHTLY,
    "month": FREQUENCY_MONTHLY,
    "quarter": FREQUENCY_QUARTERLY,
    "biannual": FREQUENCY_BIANNUAL,
    "annual": FREQUENCY_ANNUAL,
}

STATUS_COMPLETED = "completed"
STATUS_OVERDUE = "overdue"
STATUS_UPCOMING = "upcoming"
