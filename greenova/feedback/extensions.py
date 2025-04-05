"""
Jinja2 extensions for the feedback app.

This module provides filters and functions that can be used in Jinja2 templates.
"""
from typing import Dict, Union

from django.db.models import QuerySet

from .models import BugReport


def severity_color(severity: str) -> str:
    """Return a color class based on the severity level.

    Args:
        severity: The severity level string

    Returns:
        A corresponding CSS color class
    """
    colors = {
        'low': 'success',
        'medium': 'warning',
        'high': 'danger',
        'critical': 'critical',
    }
    return colors.get(severity, '')


def status_color(status: str) -> str:
    """Return a color class based on the status.

    Args:
        status: The status string

    Returns:
        A corresponding CSS color class
    """
    colors = {
        'open': 'secondary',
        'in_progress': 'primary',
        'resolved': 'success',
        'closed': 'light',
    }
    return colors.get(status, '')


def get_open_bug_count() -> int:
    """Get count of currently open bug reports.

    Returns:
        The number of bug reports with status 'open' or 'in_progress'
    """
    return BugReport.objects.filter(status__in=['open', 'in_progress']).count()


def show_bug_tracker_mini() -> Dict[str, Union[QuerySet[BugReport], int]]:
    """Get a small selection of open bug reports for mini tracker.

    Returns:
        Dictionary containing bug reports and count
    """
    bug_reports = BugReport.objects.filter(status__in=['open', 'in_progress'])[:5]
    return {
        'bug_reports': bug_reports,
        'count': bug_reports.count(),
    }


# Dictionary of all filters to be registered
feedback_filters = {
    'severity_color': severity_color,
    'status_color': status_color,
}

# Dictionary of all global functions to be registered
feedback_globals = {
    'get_open_bug_count': get_open_bug_count,
    'show_bug_tracker_mini': show_bug_tracker_mini,
}
