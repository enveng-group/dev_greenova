"""Date and time utilities for Greenova.

Provides helper functions for date and time manipulation.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from datetime import datetime, timedelta

from beartype import beartype


@beartype
def add_days_to_date(date: datetime, days: int) -> datetime:
    """Add a number of days to a datetime object.

    Args:
        date: The original datetime.
        days: Number of days to add.

    Returns:
        The new datetime after adding days.

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


@beartype
def days_between_dates(start: datetime, end: datetime) -> int:
    """Calculate the number of days between two dates.

    Args:
        start: The start datetime.
        end: The end datetime.

    Returns:
        The number of days between start and end.

    """
    return (end - start).days
