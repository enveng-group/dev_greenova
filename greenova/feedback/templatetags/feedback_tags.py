# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

"""
Django template tags and filters for the feedback app.

This module provides template tags and filters that can be used in Django templates.
"""
from typing import Dict, Union

from django import template
from django.db.models import QuerySet
from django.template.loader import render_to_string

from ..models import BugReport

register = template.Library()


@register.filter(name='severity_color')
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


@register.filter(name='status_color')
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
        'rejected': 'danger',
    }
    return colors.get(status, '')


@register.simple_tag
def get_open_bug_count() -> int:
    """Get count of currently open bug reports.

    Returns:
        The number of bug reports with status 'open' or 'in_progress'
    """
    return BugReport.objects.filter(status__in=['open', 'in_progress']).count()


@register.filter(name='get_status_description')
def get_status_description(status: str) -> str:
    """Get a descriptive text for a bug report status from plaintext template.

    Args:
        status: The status string (open, in_progress, etc.)

    Returns:
        A description of the status from the plaintext template
    """
    from feedback.views import get_status_description as get_desc
    return get_desc(status)


@register.inclusion_tag('feedback/components/bug_tracker_mini.html')
def show_bug_tracker_mini() -> Dict[str, Union[QuerySet[BugReport], int, str]]:
    """Get a small selection of open bug reports for mini tracker.

    Returns:
        Dictionary containing bug reports, count, and help text
    """
    bug_reports = BugReport.objects.filter(status__in=['open', 'in_progress'])[:5]

    # Load help text from plaintext file
    help_text = render_to_string('feedback/components/mini_tracker_help.txt')

    return {
        'bug_reports': bug_reports,
        'count': bug_reports.count(),
        'help_text': help_text,
    }
