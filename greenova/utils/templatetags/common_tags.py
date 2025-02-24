from typing import Any, Dict, List, Optional, TypeVar
from django.db.models.query import QuerySet
from django.db.models import Model
from django.template.library import Library
from django.utils.safestring import mark_safe

register = Library()

# Add the format_error filter


@register.filter
def format_error(error: str) -> str:
    """Format error message for display."""
    if not error:
        return ''
    return mark_safe(f'<mark class="error">{error}</mark>')


T = TypeVar('T', bound=Model)  # Generic type constrained to Django Models
