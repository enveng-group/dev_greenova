from django import template
from django.utils.html import format_html
from ..models import ResponsibilityAssignment

register = template.Library()


@register.filter
def user_has_responsibility(user, obligation):
    """Check if a user has any responsibility for an obligation."""
    return ResponsibilityAssignment.objects.filter(
        user=user,
        obligation=obligation
    ).exists()


@register.filter
def user_responsibility_roles(user, obligation):
    """Get a list of responsibility roles a user has for an obligation."""
    assignments = ResponsibilityAssignment.objects.filter(
        user=user,
        obligation=obligation
    ).select_related('role')
    return [assignment.role for assignment in assignments if assignment.role]


@register.filter
def format_responsibility_roles(roles):
    """Format a list of responsibility roles as HTML badges."""
    if not roles:
        return ''

    html = []
    for role in roles:
        html.append(f'<mark role="status" class="info">{role.name}</mark>')

    return format_html(' '.join(html))


@register.simple_tag
def get_responsible_users(obligation):
    """Get all users responsible for an obligation."""
    assignments = ResponsibilityAssignment.objects.filter(
        obligation=obligation
    ).select_related('user', 'role')
    return assignments
