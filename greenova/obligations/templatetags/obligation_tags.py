from datetime import date, datetime, timedelta

from beartype import beartype
from django import template
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from obligations.utils import get_responsibility_display_name

register = template.Library()


@register.filter
@beartype
def format_due_date(target_date: datetime | date | None) -> str:
    """Format due date as a simple date string.

    Args:
        target_date: Date to format, can be datetime or date object

    Returns:
        str: Formatted date string

    """
    if not target_date:
        return "No date set"

    # Convert to date if datetime
    if isinstance(target_date, datetime):
        target_date = target_date.date()

    # Just return the formatted date
    return target_date.strftime("%d %b %Y")  # Format: 01 Jan 2023


@register.filter
@beartype
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
        return 0.0


@register.inclusion_tag("obligations/components/_status_badge.html")
@beartype
def status_badge(status: str) -> dict[str, str]:
    """Return a styled status badge.

    Args:
        status: The status string

    Returns:
        Dict with status text and color class

    """
    status = status.lower() if status else ""

    if status == "not started":
        color = "warning"
    elif status == "in progress":
        color = "info"
    elif status == "completed":
        color = "success"
    elif status == "overdue":
        color = "error"
    else:
        color = "secondary"

    return {
        "status": status,
        "color": color,
    }


@register.filter
@beartype
def display_status(obligation) -> str:
    """Display an obligation status with appropriate styling.

    Checks if an obligation is overdue based on the due date and
    current status, then returns an appropriate styled status badge.
    """
    status = getattr(obligation, "status", "").lower()
    due_date = getattr(obligation, "action_due_date", None)
    today = timezone.now().date()

    # Handle overdue obligations (past due date and not completed)
    if due_date and due_date < today and status != "completed":
        return format_html(
            '<mark role="status" class="warning">Overdue</mark>',
        )

    # Handle upcoming obligations (due within 14 days)
    if due_date and today <= due_date <= today + \
            timedelta(days=14) and status != "completed":
        return format_html(
            '<mark role="status" class="info">Upcoming</mark>',
        )

    # Handle completed obligations
    if status == "completed":
        return format_html(
            '<mark role="status" class="success">Completed</mark>',
        )

    # Default status display
    if status:
        return format_html(
            '<mark role="status">{}</mark>', status.capitalize(),
        )

    # No status
    return format_html(
        '<mark role="status">Not Started</mark>',
    )


@register.filter
@beartype
def format_due_date(due_date: date | None) -> str:
    """Format a due date or indicate if it's missing."""
    if not due_date:
        return "-"

    today = timezone.now().date()

    # Check if overdue
    if due_date < today:
        return format_html(
            '<span class="overdue-date">{}</span>', due_date.strftime("%d %b %Y"),
        )

    return due_date.strftime("%d %b %Y")


@register.simple_tag
@beartype
def status_badge(status: str) -> str:
    """Generate an HTML badge based on the provided status.

    This tag takes a status string and returns an HTML span element with appropriate
    styling based on the status.
    """
    status = status.lower() if isinstance(status, str) else "unknown"

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
@beartype
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
@beartype
def get_active_obligations(active_obligations=None):
    """Return the queryset of active obligations or empty queryset."""
    return active_obligations or []


@register.simple_tag
@beartype
def get_compliance_status(compliance_status: str | None = None) -> str:
    """Return the compliance status string or 'Unknown'."""
    return compliance_status or "Unknown"


@register.simple_tag
@beartype
def get_next_due_obligation(next_due_obligation=None):
    """Return the next due obligation object or None."""
    return next_due_obligation
