from django import template

register = template.Library()

@register.filter
def display_name(user) -> str:
    """Return the best display name for a user."""
    return user.get_full_name() or user.username
