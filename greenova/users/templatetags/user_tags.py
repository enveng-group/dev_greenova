from allauth.account.models import EmailAddress
from allauth.account.utils import user_display
from django import template
from django.utils.html import format_html
from beartype import beartype

register = template.Library()


@register.filter
@beartype
def full_name_or_username(user) -> str:
    """Return user's full name or username if full name is not set.

    Args:
        user: The user object.

    Returns:
        The user's full name if set, otherwise the username.
    """
    if hasattr(user, "get_full_name") and user.get_full_name():
        return user.get_full_name()
    return user.username


@register.filter
@beartype
def profile_image_url(user) -> str:
    """Return profile image URL or empty string if no image.

    Args:
        user: The user object.

    Returns:
        The URL of the user's profile image, or an empty string.
    """
    if hasattr(user, "profile") and user.profile.profile_image:
        return user.profile.profile_image.url
    return ""


@register.simple_tag
@beartype
def user_role(user) -> str:
    """Return human-readable role for user.

    Args:
        user: The user object.

    Returns:
        The user's role as a string.
    """
    if user.is_superuser:
        return "Admin"
    if user.is_staff:
        return "Staff"
    return "User"


@register.filter
@beartype
def auth_user_display(user) -> str:
    """Return a display name for the user using allauth's user_display function.

    Args:
        user: The user object.

    Returns:
        The display name for the user.
    """
    return user_display(user)


@register.simple_tag
@beartype
def auth_status_badge(user) -> str:
    """Return an HTML badge showing the authentication status of a user.

    Args:
        user: The user object.

    Returns:
        An HTML badge as a string.
    """
    if not user.is_authenticated:
        return format_html('<span class="auth-badge auth-badge-guest">Guest</span>')

    if user.is_superuser:
        return format_html('<span class="auth-badge auth-badge-admin">Admin</span>')
    if user.is_staff:
        return format_html('<span class="auth-badge auth-badge-staff">Staff</span>')
    return format_html('<span class="auth-badge auth-badge-user">User</span>')


@register.filter
@beartype
def has_verified_email(user) -> bool:
    """Check if the user has at least one verified email address.

    Args:
        user: The user object.

    Returns:
        True if the user has a verified email, False otherwise.
    """
    if not user.is_authenticated:
        return False
    return EmailAddress.objects.filter(user=user, verified=True).exists()


@register.simple_tag(takes_context=True)
@beartype
def login_url_with_next(context) -> str:
    """Generate login URL with the current path as next parameter.

    Args:
        context: The template context.

    Returns:
        The login URL with the next parameter.
    """
    request = context.get("request")
    if not request:
        return "/authentication/login/"

    next_url = request.path
    return f"/authentication/login/?next={next_url}"


@register.simple_tag
@beartype
def get_user_profile(user_profile=None):
    """Return the user profile object or None.

    Args:
        user_profile: The user profile object.

    Returns:
        The user profile object or None.
    """
    return user_profile


@register.simple_tag
@beartype
def get_user_permissions(user_permissions=None):
    """Return the set of user permissions or empty set.

    Args:
        user_permissions: The set of user permissions.

    Returns:
        The set of user permissions or an empty set.
    """
    return user_permissions or set()


@register.simple_tag
@beartype
def get_is_admin(is_admin=None) -> bool:
    """Return True if user is admin, else False.

    Args:
        is_admin: Boolean indicating if user is admin.

    Returns:
        True if user is admin, False otherwise.
    """
    return bool(is_admin)
