from django import template
from django.utils import timezone
from datetime import datetime, date
from typing import Optional, Dict, Union
from obligations.utils import is_obligation_overdue

register = template.Library()

@register.filter
def format_due_date(target_date: Optional[Union[datetime, date]]) -> str:
    """
    Format due date as a simple date string.

    Args:
        target_date: Date to format, can be datetime or date object

    Returns:
        str: Formatted date string
    """
    if not target_date:
        return 'No date set'

    # Convert to date if datetime
    if isinstance(target_date, datetime):
        target_date = target_date.date()

    # Just return the formatted date
    return target_date.strftime('%d %b %Y')  # Format: 01 Jan 2023

@register.filter
def multiply(value, arg):
    """
    Multiply the value by the argument

    Usage: {{ value|multiply:2 }}

    Args:
        value: The value to multiply
        arg: The factor to multiply by

    Returns:
        The result of value * arg
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.inclusion_tag('obligations/components/_status_badge.html')
def status_badge(status: str) -> Dict[str, str]:
    """
    Return a styled status badge.

    Args:
        status: The status string

    Returns:
        Dict with status text and color class
    """
    status = status.lower() if status else ''

    if status == 'not started':
        color = 'warning'
    elif status == 'in progress':
        color = 'info'
    elif status == 'completed':
        color = 'success'
    elif status == 'overdue':
        color = 'error'
    else:
        color = 'secondary'

    return {
        'status': status,
        'color': color
    }

@register.inclusion_tag('obligations/components/_status_badge.html')
def display_status(obligation) -> Dict[str, str]:
    """
    Display the effective status of an obligation, showing 'overdue'
    when appropriate.

    Args:
        obligation: The obligation object

    Returns:
        Dict with status text and color class
    """
    # Check if it's overdue using the utility function
    if is_obligation_overdue(obligation):
        return {
            'status': 'overdue',
            'color': 'error'
        }
    else:
        return status_badge(obligation.status)
