import logging
from datetime import date, datetime, timedelta
from typing import Any

from beartype import beartype  # noqa: F401
from core.utils import get_responsibility_display_name
from django import template
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

register = template.Library()
logger = logging.getLogger(__name__)


@register.filter
def format_due_date(target_date: date | datetime | None) -> str:
    """Format due date as a simple date string or mark as overdue.

    Args:
        target_date: Date to format, can be datetime or date object

    Returns:
        str: Formatted date string or overdue markup

    """
    if not target_date:
        return "-"
    if isinstance(target_date, datetime):
        target_date = target_date.date()
    today = timezone.now().date()
    if target_date < today:
        return format_html(
            '<span class="overdue-date">{}</span>',
            target_date.strftime("%d %b %Y"),
        )
    return target_date.strftime("%d %b %Y")


@register.filter
def multiply(value: float, arg: float) -> float:
    """Multiply the value by the argument.

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
        logger.warning("multiply filter received invalid input: %r, %r", value, arg)
        return 0.0


@register.filter
def display_status(obligation: Any) -> str:
    """Display an obligation status with appropriate styling.

    Args:
        obligation: Obligation instance

    Returns:
        str: HTML markup for status

    """
    status = getattr(obligation, "status", "").lower()
    due_date = getattr(obligation, "action_due_date", None)
    today = timezone.now().date()
    if due_date and due_date < today and status != "completed":
        return format_html(
            '<mark role="status" class="{}">{}</mark>',
            "warning",
            "Overdue",
        )
    if (
        due_date
        and today <= due_date <= today + timedelta(days=14)
        and status != "completed"
    ):
        return format_html(
            '<mark role="status" class="{}">{}</mark>',
            "info",
            "Upcoming",
        )
    if status == "completed":
        return format_html(
            '<mark role="status" class="{}">{}</mark>',
            "success",
            "Completed",
        )
    if status:
        return format_html('<mark role="status">{}</mark>', status.capitalize())
    return format_html('<mark role="status">{}</mark>', "Not Started")


@register.simple_tag
def status_badge(status: str) -> str:
    """Generate an HTML badge based on the provided status.

    Args:
        status: The status string

    Returns:
        str: HTML markup for badge

    """
    status = status.lower() if status else "unknown"
    badge_classes = {
        "completed": "status-badge status-completed",
        "in progress": "status-badge status-in-progress",
        "not started": "status-badge status-not-started",
        "overdue": "status-badge status-overdue",
        "unknown": "status-badge status-unknown",
    }
    badge_class = badge_classes.get(status, badge_classes["unknown"])
    return mark_safe(f'<span class="{badge_class}">{status}</span>')


@register.filter
def display_responsibility(responsibility: str | None) -> str:
    """Format the responsibility value for display.

    Args:
        responsibility: The responsibility value from an obligation

    Returns:
        str: Formatted string for display

    """
    if not responsibility:
        return "-"
    return get_responsibility_display_name(responsibility)


@register.simple_tag
def get_active_obligations(active_obligations: Any = None) -> Any:
    """Return the queryset of active obligations or empty queryset."""
    return active_obligations or []


@register.simple_tag
def get_compliance_status(compliance_status: str | None = None) -> str:
    """Return the compliance status string or 'Unknown'."""
    return compliance_status or "Unknown"


@register.simple_tag
def get_next_due_obligation(next_due_obligation: Any = None) -> Any:
    """Return the next due obligation object or None."""
    return next_due_obligation
