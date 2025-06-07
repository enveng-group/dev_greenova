"""Utility functions related to obligations."""

from datetime import date


def is_obligation_overdue(due_date: date) -> bool:
    """Check if an obligation is overdue.

    Args:
        due_date: The due date of the obligation.

    Returns:
        True if the obligation is overdue, False otherwise.

    """
    return due_date < date.today()
