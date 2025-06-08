"""Date and time utilities for Greenova.

Provides helper functions for date and time manipulation.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from datetime import datetime, timedelta

from beartype import beartype


@beartype
def add_days_to_date(date: datetime, days: int) -> datetime:
    """Add a specified number of days to a date.

    Args:
        date: The original date.
        days: The number of days to add.

    Returns:
        A new datetime object with the days added.

    """
    return date + timedelta(days=days)


@beartype
def format_date(date: datetime, format_string: str = "%Y-%m-%d") -> str:
    """Format a datetime object as a string.

    Args:
        date: The datetime object to format.
        format_string: The format string to use.

    Returns:
        A formatted date string.

    """
    return date.strftime(format_string)
