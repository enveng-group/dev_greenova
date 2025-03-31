from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def user_has_responsibility(user, obligation):
    """Check if a user has any responsibility for an obligation."""
    # Simplified implementation without ResponsibilityAssignment
    return False


@register.simple_tag
def user_responsibility_roles(user, obligation):
    """Get responsibility roles for a user and obligation."""
    # Simplified implementation without ResponsibilityAssignment
    return []


@register.simple_tag
def get_responsible_users(obligation):
    """Get all users responsible for an obligation."""
    # Simplified implementation without ResponsibilityAssignment
    return []


@register.simple_tag
def format_responsibility_roles(roles):
    """Format a list of responsibility roles as HTML."""
    if not roles:
        return ''

    html = ''
    for role in roles:
        html += format_html('<mark class="responsibility-role">{}</mark> ', role.name)

    return html
