from django import template
from django.utils import timezone
from datetime import datetime
from typing import Optional, Dict

register = template.Library()

@register.filter
def format_status(status: str) -> str:
    """Format status for display."""
    return status.replace('_', ' ').title()

@register.filter
def format_due_date(date: Optional[datetime]) -> str:
    """Format due date with color coding."""
    if not date:
        return 'No date set'

    today = timezone.now().date()
    days_until = (date.date() - today).days

    if days_until < 0:
        return f'Overdue by {abs(days_until)} days'
    elif days_until == 0:
        return 'Due today'
    else:
        return f'Due in {days_until} days'

@register.inclusion_tag('obligations/components/_status_badge.html')
def status_badge(status: str) -> Dict[str, str]:
    """Render status badge."""
    colors = {
        'not started': 'warning',
        'in progress': 'info',
        'completed': 'success'
    }
    return {
        'status': status,
        'color': colors.get(status, 'secondary')
    }
