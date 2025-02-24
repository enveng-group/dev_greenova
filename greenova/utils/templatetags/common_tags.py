from typing import Any, Dict, List, Optional, TypeVar
from django.db.models.query import QuerySet
from django.db.models import Model
from django.template.library import Library

register = Library()

T = TypeVar('T', bound=Model)  # Generic type constrained to Django Models

@register.inclusion_tag('components/data_table.html')
def data_table(
    data: QuerySet[T],
    headers: List[str],
    title: str,
    empty_message: Optional[str] = None
) -> Dict[str, Any]:
    """
    Renders a data table component.

    Args:
        data: QuerySet containing model instances to display
        headers: List of column headers
        title: Title of the data table
        empty_message: Optional message to display when data is empty

    Returns:
        Dict containing template context variables
    """
    return {
        'data': data,
        'headers': headers,
        'title': title,
        'empty_message': empty_message
    }

@register.inclusion_tag('components/dialogs/base_dialog.html')
def modal_dialog(
    dialog_id: str,
    title: str,
    content_template: str,
    **kwargs: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Renders a modal dialog component.

    Args:
        dialog_id: Unique identifier for the dialog
        title: Dialog title
        content_template: Template path for dialog content
        **kwargs: Additional template context variables

    Returns:
        Dict containing template context variables
    """
    return {
        'dialog_id': dialog_id,
        'title': title,
        'content_template': content_template,
        **kwargs
    }
