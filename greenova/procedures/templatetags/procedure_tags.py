# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

"""
Django template tags and filters for the procedures app.

This module provides template tags and filters that can be used in Django templates
for procedure-related functionality.
"""
from typing import Any, Dict

from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def format_procedure_name(name: str) -> str:
    """
    Convert procedure name to a more readable format.

    Args:
        name: The procedure name to format

    Returns:
        Formatted procedure name
    """
    return name.replace('_', ' ').title()


@register.filter
def format_procedure_status(status: str) -> str:
    """
    Format procedure status with appropriate styling.

    Args:
        status: The status to format

    Returns:
        Formatted status string
    """
    statuses = {
        'not started': 'Not Started',
        'in progress': 'In Progress',
        'completed': 'Completed',
        'on hold': 'On Hold'
    }
    return statuses.get(status.lower(), status)


@register.simple_tag
def procedure_status_badge(status: str) -> str:
    """
    Generate HTML for a procedure status badge.

    Args:
        status: The status to create a badge for

    Returns:
        HTML for the status badge
    """
    status_colors = {
        'not started': 'warning',
        'in progress': 'info',
        'completed': 'success',
        'on hold': 'secondary',
        'overdue': 'error'
    }

    formatted_status = format_procedure_status(status)
    color_class = status_colors.get(status.lower(), 'secondary')

    return format_html('<span class="status-badge {}">{}</span>',
                       color_class, formatted_status)


@register.inclusion_tag('procedures/components/procedure_stats.html')
def procedure_stats(stats: Dict[str, int]) -> Dict[str, Any]:
    """
    Render procedure statistics.

    Args:
        stats: Dictionary with status counts

    Returns:
        Context for the template
    """
    return {'stats': stats}


@register.inclusion_tag('procedures/components/procedure_chart_card.html')
def procedure_chart_card(procedure: Dict[str, Any]) -> Dict[str, Any]:
    """
    Render a procedure chart card.

    Args:
        procedure: Dictionary with procedure data

    Returns:
        Context for the template
    """
    return {'procedure': procedure}
