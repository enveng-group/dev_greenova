"""Django template tags and filters for the mechanisms app.

Provides custom template tags and filters for rendering mechanism-related data
in Django templates, including status formatting, obligation counts, and color
classes for mechanism statuses.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from typing import Any

from beartype import beartype
from django import template
from mechanisms.models import EnvironmentalMechanism

logger = logging.getLogger(__name__)

register = template.Library()


@register.filter
@beartype
def get_item(dictionary: dict[str, Any], key: Any) -> Any:
    """Get item from dictionary by key.

    Args:
        dictionary: The dictionary to retrieve the item from.
        key: The key to look up in the dictionary.

    Returns:
        The value associated with the key, or None if not found.

    """
    return dictionary.get(key)


@register.filter
@beartype
def mechanism_name(mechanism_id: int) -> str:
    """Get mechanism name by ID.

    Args:
        mechanism_id: The ID of the mechanism.

    Returns:
        The name of the mechanism, or a fallback string if not found.

    """
    try:
        mechanism: EnvironmentalMechanism = EnvironmentalMechanism.objects.get(
            id=mechanism_id,
        )  # type: ignore[attr-defined]
        return mechanism.name  # type: ignore[attr-defined]
    except EnvironmentalMechanism.DoesNotExist:
        logger.warning("Mechanism with ID %d does not exist.", mechanism_id)
        return "Unknown Mechanism"
    except ValueError:
        logger.exception("Invalid mechanism ID: %r", mechanism_id)
        return "Invalid ID"


@register.filter
@beartype
def format_count(count: int) -> str:
    """Format count number with appropriate styling class.

    Args:
        count: The count value to format.

    Returns:
        HTML string with appropriate class for zero/nonzero counts.

    """
    if count == 0:
        logger.info("Count is zero; applying zero styling.")
        return '<span class="count-zero">0</span>'
    return f'<span class="count-nonzero">{count}</span>'


@register.filter
@beartype
def total_obligations(mechanism: EnvironmentalMechanism) -> int:
    """Get total obligations for a mechanism.

    Args:
        mechanism: The EnvironmentalMechanism instance.

    Returns:
        The total number of obligations for the mechanism.

    """
    try:
        return mechanism.total_obligations  # type: ignore[attr-defined]
    except Exception as exc:
        logger.exception(
            "Error getting obligations for mechanism %r: %s",
            mechanism,
            exc,
        )
        return 0


@register.inclusion_tag("mechanisms/components/mechanism_card.html")
@beartype
def mechanism_card(mechanism: Any) -> dict[str, Any]:
    """Render a mechanism card component.

    Args:
        mechanism: The EnvironmentalMechanism instance.

    Returns:
        Context dictionary for the mechanism card template.

    """
    mechanism_id = getattr(mechanism, "id", None)
    logger.info("Rendering mechanism card for mechanism ID %r.", mechanism_id)
    return {"mechanism": mechanism}


@register.inclusion_tag("mechanisms/components/mechanism_table.html")
@beartype
def mechanism_table(mechanisms: Any) -> dict[str, Any]:
    """Render a table of mechanisms.

    Args:
        mechanisms: QuerySet of EnvironmentalMechanism instances.

    Returns:
        Context dictionary for the mechanism table template.

    """
    count = getattr(mechanisms, "count", lambda: len(mechanisms))()
    logger.info("Rendering mechanism table for %d mechanisms.", count)
    return {"mechanisms": mechanisms}


@register.filter
@beartype
def get_status_color(status: str) -> str:
    """Get appropriate color class for status.

    Args:
        status: The status string (e.g., 'Not Started', 'Completed').

    Returns:
        The CSS class name for the given status.

    """
    color_map: dict[str, str] = {
        "Not Started": "status-not-started",
        "In Progress": "status-in-progress",
        "Completed": "status-completed",
        "Overdue": "status-overdue",
    }
    color = color_map.get(status, "status-unknown")
    logger.debug("Status '%s' mapped to color '%s'", status, color)
    return color
