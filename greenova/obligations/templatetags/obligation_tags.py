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

@register.inclusion_tag('obligations/components/_status_badge.html')
def status_badge(status: str) -> Dict[str, str]:
    """
    Render status badge with proper styling.

    Args:
        status: Current status string

    Returns:
        Dict containing formatted status and color class
    """
    colors: Dict[str, str] = {
        'not started': 'warning',
        'in progress': 'info',
        'completed': 'success',
        'on hold': 'secondary',
        'cancelled': 'danger',
        'overdue': 'danger'  # Add overdue status with danger color
    }

    formatted_status = status.replace('_', ' ').title()
    color = colors.get(status.lower(), 'secondary')

    return {
        'status': formatted_status,
        'color': color
    }

@register.filter
def display_status(obligation) -> str:
    """
    Determine the display status of an obligation, showing 'overdue' for
    past-due obligations that aren't completed.

    Args:
        obligation: The obligation object

    Returns:
        str: Status for display, including 'Overdue' when applicable
    """
    # Use the utility function to check if obligation is overdue
    if is_obligation_overdue(obligation):
        return 'overdue'

    # Otherwise return the original status
    return obligation.status
