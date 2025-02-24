from django import template
from django.forms import BoundField
from typing import Optional, Dict, Any

register = template.Library()

@register.inclusion_tag('authentication/components/forms/field.html')
def render_field(field: BoundField, help_text: Optional[str] = None) -> Dict[str, Any]:
    """
    Renders a form field with optional help text.

    Args:
        field: The form field to render
        help_text: Optional help text to display

    Returns:
        Dictionary containing field data for template
    """
    return {
        'field': field,
        'field_id': field.auto_id,
        'help_text': help_text or field.help_text,
        'errors': field.errors
    }
