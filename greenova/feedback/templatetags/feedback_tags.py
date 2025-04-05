from typing import QuerySet

from django import template

from ..models import BugReport  # Ensure the correct relative import path

register = template.Library()


@register.filter
def severity_color(severity):
    """
    Return a color class based on the severity level.
    """
    colors = {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger',
        'critical': 'critical',
    }
    return colors.get(severity, '')


@register.filter
def status_color(status):
    """
    Return a color class based on the status.
    """
    colors = {
        'open': 'secondary',
        'in_progress': 'primary',
        'resolved': 'success',
        'closed': 'light',
    }
    return colors.get(status, '')


def get_open_bug_count() -> int:
    return BugReport.objects.filter(status__in=['open', 'in_progress']).count()


def show_bug_tracker_mini() -> dict[str, QuerySet[BugReport] | int]:
    bug_reports = BugReport.objects.filter(status__in=['open', 'in_progress'])[:5]
    return {
        'bug_reports': bug_reports,
        'count': bug_reports.count(),
    }
