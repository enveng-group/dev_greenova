"""Frequency normalization utilities for Greenova.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype


@beartype
def normalize_frequency(frequency: str) -> str:
    """Normalize frequency string to canonical value.

    Args:
        frequency: Input frequency string (case-insensitive).

    Returns:
        Canonical frequency string (e.g., 'daily', 'weekly', etc.).

    """
    freq = frequency.strip().lower()
    if freq in {"daily", "day"}:
        return "daily"
    if freq in {"weekly", "week"}:
        return "weekly"
    if freq in {"monthly", "month"}:
        return "monthly"
    if freq in {"quarterly", "quarter"}:
        return "quarterly"
    if freq in {"annually", "annual", "yearly", "year"}:
        return "annually"
    return freq
