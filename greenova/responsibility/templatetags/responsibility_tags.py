from django import template
from django.utils.html import format_html

from ..models import Responsibility

register = template.Library()


@register.filter
def user_has_responsibility(user, obligation):
    """Check if a user has any responsibility for an obligation."""
    return ResponsibilityAssignment.objects.filter(
        user=user,
        obligation=obligation
    ).exists()


@register.simple_tag
def get_responsible_users(obligation):
    """Get all users responsible for an obligation."""
    assignments = ResponsibilityAssignment.objects.filter(
        obligation=obligation
    ).select_related('user', 'role')
    return assignments
