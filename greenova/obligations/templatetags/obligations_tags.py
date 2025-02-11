from datetime import date, datetime, timedelta

from django import template
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.timezone import now

register = template.Library()


@register.filter
def status_class(status):
    """Return CSS class based on obligation status."""
    if not status:
        return 'status-unknown'

    status_classes = {
        'not started': 'status-not-started',
        'in progress': 'status-in-progress',
        'completed': 'status-completed',
    }
    return status_classes.get(status.lower(), 'status-unknown')


@register.filter
def due_date_class(due_date):
    """Return CSS class based on due date proximity."""
    if not due_date:
        return 'no-date'

    today = now().date()
    days_until = (due_date - today).days

    if days_until < 0:
        return 'overdue'
    elif days_until <= 7:
        return 'due-soon'
    elif days_until <= 14:
        return 'upcoming'
    return 'future'


@register.simple_tag
def obligation_card(obligation):
    """Generate an obligation card with status and due date indicators."""
    status_class_name = status_class(obligation.status)
    due_class = due_date_class(obligation.action_due_date)

    return format_html(
        '<article class="obligation-card {}">'
        '  <header class="card-header">'
        '    <h3>{}</h3>'
        '    <span class="status-badge {}">{}</span>'
        '  </header>'
        '  <div class="card-body">'
        '    <p>{}</p>'
        '    <div class="due-date {}">'
        '      Due: {}'
        '    </div>'
        '  </div>'
        '</article>',
        due_class,
        obligation.obligation_number,
        status_class_name,
        obligation.status,
        obligation.obligation,
        due_class,
        (
            obligation.action_due_date.strftime('%d %b %Y')
            if obligation.action_due_date
            else 'No due date'
        ),
    )


@register.simple_tag
def obligation_stats(obligations):
    """Generate statistics for obligations."""
    total = len(obligations)
    completed = sum(1 for o in obligations if o.status == 'completed')
    overdue = sum(1 for o in obligations if o.is_overdue())

    return {
        'total': total,
        'completed': completed,
        'overdue': overdue,
        'completion_rate': (completed / total * 100) if total > 0 else 0,
    }


@register.filter
def format_frequency(frequency):
    """Format recurring frequency in a human-readable way."""
    if not frequency:
        return 'Not specified'

    frequencies = {
        'daily': 'Daily',
        'weekly': 'Weekly',
        'monthly': 'Monthly',
        'quarterly': 'Quarterly',
        'annually': 'Annually',
    }
    return frequencies.get(
        frequency.lower(), frequency.replace('_', ' ').title()
    )
