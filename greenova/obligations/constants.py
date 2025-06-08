"""Constants for the obligations app.

Defines static values and choices for obligation models and logic.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>

License:
    AGPL-3.0
"""

# Only import what is used from core.constants
from core.constants import STATUS_NOT_STARTED

OBLIGATION_DEFAULT_STATUS = STATUS_NOT_STARTED

# Frequency constants and aliases (obligation-specific)
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
