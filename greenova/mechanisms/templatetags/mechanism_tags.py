from typing import Dict, TypeVar
from django import template

register = template.Library()

K = TypeVar('K')  # Key type
V = TypeVar('V')  # Value type

@register.filter
def get_item(dictionary: Dict[K, V], key: K) -> V | None:
    """
    Get item from dictionary by key.

    Args:
        dictionary: Dictionary to get value from
        key: Key to look up in the dictionary

    Returns:
        Value associated with key if found, None otherwise
    """
    return dictionary.get(key)
