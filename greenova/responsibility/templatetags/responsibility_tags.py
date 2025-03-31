from django import template
from django.utils.html import format_html
<<<<<<< HEAD
=======
from ..models import ResponsibilityAssignment
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

register = template.Library()


@register.filter
def user_has_responsibility(user, obligation):
    """Check if a user has any responsibility for an obligation."""
<<<<<<< HEAD
    # Simplified implementation without ResponsibilityAssignment
    return False


@register.simple_tag
def user_responsibility_roles(user, obligation):
    """Get responsibility roles for a user and obligation."""
    # Simplified implementation without ResponsibilityAssignment
    return []
=======
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
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))


@register.simple_tag
def get_responsible_users(obligation):
    """Get all users responsible for an obligation."""
<<<<<<< HEAD
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
=======
    assignments = ResponsibilityAssignment.objects.filter(
        obligation=obligation
    ).select_related('user', 'role')
    return assignments
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
