"""Utility functions for the obligations app.

Provides helpers for status, frequency normalization, and responsibility display.
"""

from datetime import date
from typing import cast

from beartype import beartype
from constants import FREQUENCY_ALIASES
from models import Obligation


@beartype
def normalize_frequency(frequency: str) -> str:
    """Normalize frequency string to canonical value used in the system.

    Args:
        frequency: The frequency string to normalize.

    Returns:
        The canonical frequency string.
    """
    freq = frequency.strip().lower().replace(" ", "-")
    # Explicitly cast to str to satisfy type checker
    return cast(str, FREQUENCY_ALIASES.get(freq, freq))


@beartype
def is_obligation_overdue(obligation: Obligation) -> bool:
    """Check if an obligation is overdue.

    Args:
        obligation: The Obligation instance to check.

    Returns:
        True if the obligation is overdue, False otherwise.
    """
    if not obligation.action_due_date:
        return False
    if obligation.status == "completed":
        return False
    # Ensure the comparison returns a bool
    return bool(obligation.action_due_date < date.today())
