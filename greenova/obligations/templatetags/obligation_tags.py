from django import template
from django.utils import timezone
from datetime import datetime, date
from typing import Optional, Dict, Any, Union

register = template.Library()

@register.filter
def format_due_date(target_date: Optional[Union[datetime, date]]) -> str:
    """
    Format due date with color coding.

    Args:
        target_date: Date to format, can be datetime or date object

    Returns:
        str: Formatted date string with relative days
    """
    if not target_date:
        return 'No date set'

    today = timezone.now().date()

    # Convert to date if datetime
    if isinstance(target_date, datetime):
        target_date = target_date.date()

    days_until = (target_date - today).days

    if days_until < 0:
        return f'Overdue by {abs(days_until)} days'
    elif days_until == 0:
        return 'Due today'
    else:
        return f'Due in {days_until} days'

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
        'cancelled': 'danger'
    }

    formatted_status = status.replace('_', ' ').title()
    color = colors.get(status.lower(), 'secondary')

    return {
        'status': formatted_status,
        'color': color
    }
