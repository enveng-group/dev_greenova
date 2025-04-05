"""
Jinja2 extensions for the dashboard app.

This module provides filters and functions that can be used in Jinja2 templates.
"""
from typing import Any


def display_name(user: Any) -> str:
    """Return the best display name for a user.

    Args:
        user: A Django user or any object with name attributes

    Returns:
        The full name if available, otherwise username or string representation
    """
    if hasattr(user, 'get_full_name'):
        full_name = user.get_full_name()
        if full_name:
            return full_name
    return user.username if hasattr(user, 'username') else str(user)


def format_date(date_value: Any, format_string: str = '%d %b %Y') -> str:
    """Format a date with a specified format string.

    Args:
        date_value: A date object to format
        format_string: The format string to use

    Returns:
        Formatted date string or empty string if date is None
    """
    if date_value is None:
        return ''
    try:
        return date_value.strftime(format_string)
    except (AttributeError, ValueError):
        return str(date_value)


# Dictionary of all filters to be registered
dashboard_filters = {
    'display_name': display_name,
    'format_date': format_date,
}

# Dictionary of all global functions to be registered
dashboard_globals: dict[str, Any] = {
    # Add any global functions here
}
