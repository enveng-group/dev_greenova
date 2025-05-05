from datetime import date, datetime, timedelta
from typing import Optional, Union

from django import template
from django.utils import timezone
from django.utils.html import escape, format_html
from obligations.utils import get_responsibility_display_name

register = template.Library()

@register.filter
def format_due_date(target_date: Optional[Union[datetime, date]]) -> str:
    """
    Format due date as a simple date string or indicate if it's missing/overdue.

    Args:
        target_date: Date to format, can be datetime or date object

    Returns:
        str: Formatted date string with appropriate styling if overdue
    """
    if not target_date:
        return 'No date set'

    # Convert to date if datetime
    if isinstance(target_date, datetime):
        target_date = target_date.date()

    today = timezone.now().date()

    # Check if overdue
    if target_date < today:
        return format_html(
            '<span class="overdue-date">{}</span>', target_date.strftime('%d %b %Y')
        )

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

@register.simple_tag
def status_badge(status: str) -> str:
    """
    Generate an HTML badge based on the provided status.

    This tag takes a status string and returns an HTML span element with appropriate
    styling based on the status.

    Args:
        status: The status string

    Returns:
        str: HTML formatted status badge
    """
    status = status.lower() if isinstance(status, str) else 'unknown'

    badge_classes = {
        'completed': 'status-badge status-completed',
        'in progress': 'status-badge status-in-progress',
        'not started': 'status-badge status-not-started',
        'overdue': 'status-badge status-overdue',
        'unknown': 'status-badge status-unknown'
    }

    badge_class = badge_classes.get(status, badge_classes['unknown'])

    # Use format_html to safely generate the HTML
    return format_html('<span class="{}">{}</span>', badge_class, escape(status))

@register.filter
def display_status(obligation):
    """
    Display an obligation status with appropriate styling.

    Checks if an obligation is overdue based on the due date and
    current status, then returns an appropriate styled status badge.
    """
    status = getattr(obligation, 'status', '').lower()
    due_date = getattr(obligation, 'action_due_date', None)
    today = timezone.now().date()

    # Handle overdue obligations (past due date and not completed)
    if due_date and due_date < today and status != 'completed':
        return format_html(
            '<mark role="status" class="warning">Overdue</mark>'
        )

    # Handle upcoming obligations (due within 14 days)
    elif due_date and today <= due_date <= today + timedelta(days=14) and status != 'completed':
        return format_html(
            '<mark role="status" class="info">Upcoming</mark>'
        )

    # Handle completed obligations
    elif status == 'completed':
        return format_html(
            '<mark role="status" class="success">Completed</mark>'
        )

    # Default status display
    elif status:
        return format_html(
            '<mark role="status">{}</mark>', status.capitalize()
        )

    # No status
    else:
        return format_html(
            '<mark role="status">Not Started</mark>'
        )

@register.filter
def display_responsibility(responsibility):
    """
    Format the responsibility value for display.

    Args:
        responsibility: The responsibility value from an obligation

    Returns:
        str: Formatted string for display
    """
    if not responsibility:
        return '-'

    return get_responsibility_display_name(responsibility)
