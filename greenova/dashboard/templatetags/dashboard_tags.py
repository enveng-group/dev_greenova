from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter
def display_name(user: User) -> str:
    """Return the best display name for a user."""
    if hasattr(user, 'get_full_name'):
        full_name = user.get_full_name()
        if full_name:
            return full_name
    return user.username if hasattr(user, 'username') else str(user)
