# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: 	AGPL-3.0-or-later

"""
Django template tags and filters for the dashboard app.

This module provides template tags and filters that can be used in Django templates.
"""
from typing import Any

from beartype import beartype
from django import template
from users.utils import calculate_overdue_obligations

register = template.Library()


@register.filter(name='display_name')
def display_name(user: Any) -> str:
    """Return the best display name for a user.

    Args:
        user: A Django user or any object with name attributes.

    Returns:
        The full name if available, otherwise username or string representation.
    """
    if hasattr(user, 'get_full_name'):
        full_name = user.get_full_name()
        if full_name:
            return str(full_name)
    if hasattr(user, 'username'):
        return str(user.username)
    return str(user)


@register.filter(name='format_date')
def format_date(date_value: Any, format_string: str = '%d %b %Y') -> str:
    """Format a date with a specified format string.

    Args:
        date_value: A date object to format.
        format_string: The format string to use.

    Returns:
        Formatted date string or empty string if date is None.
    """
    if date_value is None:
        return ''
    try:
        return str(date_value.strftime(format_string))
    except (AttributeError, ValueError):
        return str(date_value)


@register.simple_tag(takes_context=True)
@beartype
def get_overdue_obligations_for_user(context: dict[str, Any]) -> list[Any]:
    """Return a queryset of overdue obligations for the authenticated user.

    Args:
        context: The template context, must include 'request'.

    Returns:
        A list or queryset of overdue obligations for the authenticated user,
        or an empty list if the user is not authenticated.
    """
    user = context['request'].user
    if not user.is_authenticated:
        return []
    return list(calculate_overdue_obligations(user.id))
