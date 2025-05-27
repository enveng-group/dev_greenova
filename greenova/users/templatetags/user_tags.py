"""Template tags for user display and authentication in Greenova users app.

Provides filters and tags for displaying user information, roles, authentication status,
and verified email status in Django templates.
"""

from allauth.account.models import EmailAddress
from allauth.account.utils import user_display
from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter
def full_name_or_username(user):
    """Return user's full name or username if full name is not set.

    Args:
        user: The user object to display.

    Returns:
        The user's full name if available, otherwise the username.
    """
    if hasattr(user, "get_full_name") and user.get_full_name():
        return user.get_full_name()
    return user.username


@register.filter
def profile_image_url(user):
    """Return profile image URL or empty string if no image.

    Args:
        user: The user object whose profile image is requested.

    Returns:
        The URL of the user's profile image, or an empty string if not set.
    """
    if hasattr(user, "profile") and user.profile.profile_image:
        return user.profile.profile_image.url
    return ""


@register.simple_tag
def user_role(user):
    """Return human-readable role for user.

    Args:
        user: The user object whose role is to be determined.

    Returns:
        A string representing the user's role: 'Admin', 'Staff', or 'User'.
    """
    if user.is_superuser:
        return "Admin"
    if user.is_staff:
        return "Staff"
    return "User"


@register.filter
def auth_user_display(user):
    """Return a display name for the user using allauth's user_display function.

    Args:
        user: The user object to display.

    Returns:
        The display name for the user, as determined by allauth's user_display.
    """
    return user_display(user)


@register.simple_tag
def auth_status_badge(user):
    """Return an HTML badge showing the authentication status of a user.

    Args:
        user: The user object whose authentication status is to be displayed.

    Returns:
        An HTML string representing the user's authentication status badge.
    """
    if not user.is_authenticated:
        return format_html('<span class="auth-badge auth-badge-guest">Guest</span>')

    if user.is_superuser:
        return format_html('<span class="auth-badge auth-badge-admin">Admin</span>')
    if user.is_staff:
        return format_html('<span class="auth-badge auth-badge-staff">Staff</span>')
    return format_html('<span class="auth-badge auth-badge-user">User</span>')


@register.filter
def has_verified_email(user):
    """Check if the user has at least one verified email address.

    Args:
        user: The user object to check for verified email addresses.

    Returns:
        True if the user has at least one verified email address, False otherwise.
    """
    if not user.is_authenticated:
        return False
    return EmailAddress.objects.filter(user=user, verified=True).exists()


@register.simple_tag(takes_context=True)
def login_url_with_next(context):
    """Generate login URL with the current path as next parameter.

    Args:
        context: The template context, expected to contain the request object.

    Returns:
        A login URL with the current path as the 'next' parameter.
    """
    request = context.get("request")
    if not request:
        return "/authentication/login/"

    next_url = request.path
    return f"/authentication/login/?next={next_url}"
