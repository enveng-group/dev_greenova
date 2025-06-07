"""Frequency normalization utilities for Greenova.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype


@beartype
def normalize_frequency(frequency: str) -> str:
    """Normalize a frequency string to its canonical form.

    This handles variations in terminology and ensures consistency
    across the application.

    Args:
        frequency: A string representing the frequency

    Returns:
        str: The normalized frequency string

    """
    from core.constants import (
        FREQUENCY_ALIASES,
        FREQUENCY_ANNUAL,
        FREQUENCY_BIANNUAL,
        FREQUENCY_DAILY,
        FREQUENCY_FORTNIGHTLY,
        FREQUENCY_MONTHLY,
        FREQUENCY_QUARTERLY,
        FREQUENCY_WEEKLY,
    )

    if not frequency:
        return ""
    frequency_lower = frequency.lower().strip()
    if frequency_lower in {
        FREQUENCY_DAILY,
        FREQUENCY_WEEKLY,
        FREQUENCY_FORTNIGHTLY,
        FREQUENCY_MONTHLY,
        FREQUENCY_QUARTERLY,
        FREQUENCY_BIANNUAL,
        FREQUENCY_ANNUAL,
    }:
        return frequency_lower
    for alias, canonical in FREQUENCY_ALIASES.items():
        if alias in frequency_lower:
            return canonical
    if "day" in frequency_lower or "daily" in frequency_lower:
        return FREQUENCY_DAILY
    if "week" in frequency_lower:
        return FREQUENCY_WEEKLY
    if (
        "fortnight" in frequency_lower
        or "bi-week" in frequency_lower
        or "biweek" in frequency_lower
    ):
        return FREQUENCY_FORTNIGHTLY
    if "month" in frequency_lower:
        return FREQUENCY_MONTHLY
    if (
        "quarter" in frequency_lower
        or "3 month" in frequency_lower
        or "three month" in frequency_lower
    ):
        return FREQUENCY_QUARTERLY
    if (
        "biannual" in frequency_lower
        or "bi annual" in frequency_lower
        or "semi" in frequency_lower
        or "twice a year" in frequency_lower
        or "6 month" in frequency_lower
    ):
        return FREQUENCY_BIANNUAL
    if (
        "annual" in frequency_lower
        or "year" in frequency_lower
        or "12 month" in frequency_lower
        or "twelve month" in frequency_lower
    ):
        return FREQUENCY_ANNUAL
    return frequency_lower
