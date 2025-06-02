from typing import Any

from django import template

register = template.Library()


@register.inclusion_tag("chatbot/chat_widget.html")
def chat_widget() -> dict[str, Any]:
    """Render the chat widget."""
    return {}
