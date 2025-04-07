from typing import Any, Dict

from django import template
from django.db.models import QuerySet

from ..models import EnvironmentalMechanism

register = template.Library()


@register.filter
def get_item(dictionary: Dict[str, Any], key: Any) -> Any:
    """Get item from dictionary by key."""
    return dictionary.get(key)


@register.filter
def mechanism_name(mechanism_id: int) -> str:
    """Get mechanism name by ID."""
    try:
        mechanism = EnvironmentalMechanism.objects.get(id=mechanism_id)
        return mechanism.name
    except EnvironmentalMechanism.DoesNotExist:
        return 'Unknown Mechanism'
    except ValueError:
        return 'Error retrieving mechanism'


@register.filter
def format_count(count: int) -> str:
    """Format count number with appropriate styling class."""
    if count == 0:
        return f'<span class="count-zero">{count}</span>'
    return f'<span class="count-nonzero">{count}</span>'


@register.filter
def total_obligations(mechanism: EnvironmentalMechanism) -> int:
    """Get total obligations for a mechanism."""
    return mechanism.total_obligations


@register.inclusion_tag('mechanisms/components/mechanism_card.html')
def mechanism_card(mechanism: EnvironmentalMechanism) -> Dict[str, Any]:
    """Render a mechanism card with status counts."""
    status_data = mechanism.get_status_data()
    return {
        'mechanism': mechanism,
        'status_data': status_data,
    }


@register.inclusion_tag('mechanisms/components/mechanism_table.html')
def mechanism_table(mechanisms: QuerySet[EnvironmentalMechanism]) -> Dict[str, Any]:
    """Render a table of mechanisms with their status counts."""
    return {'mechanisms': mechanisms}


@register.filter
def get_status_color(status: str) -> str:
    """Get appropriate color class for status."""
    status_colors = {
        'Not Started': 'warning',
        'In Progress': 'info',
        'Completed': 'success',
        'Overdue': 'error',
    }
    return status_colors.get(status, 'secondary')
