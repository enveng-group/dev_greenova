from django import template
from django.contrib.auth.models import User
from django.utils.html import format_html
from allauth.account.utils import user_display

register = template.Library()


@register.filter
def full_name_or_username(user):
    """Return user's full name or username if full name is not set."""
    if hasattr(user, 'get_full_name') and user.get_full_name():
        return user.get_full_name()
    return user.username


@register.filter
def profile_image_url(user):
    """Return profile image URL or empty string if no image."""
    if hasattr(user, 'profile') and user.profile.profile_image:
        return user.profile.profile_image.url
    return ''


@register.simple_tag
def user_role(user):
    """Return human-readable role for user."""
    if user.is_superuser:
        return "Admin"
    elif user.is_staff:
        return "Staff"
    else:
        return "User"


@register.filter
def auth_user_display(user):
    """
    Return a display name for the user using allauth's user_display function.
    This is more robust than manually checking for full_name.
    """
    return user_display(user)


@register.simple_tag
def auth_status_badge(user):
    """Return an HTML badge showing the authentication status of a user."""
    if not user.is_authenticated:
        return format_html('<span class="auth-badge auth-badge-guest">Guest</span>')

    if user.is_superuser:
        return format_html('<span class="auth-badge auth-badge-admin">Admin</span>')
    elif user.is_staff:
        return format_html('<span class="auth-badge auth-badge-staff">Staff</span>')
    else:
        return format_html('<span class="auth-badge auth-badge-user">User</span>')


@register.filter
def has_verified_email(user):
    """Check if the user has at least one verified email address."""
    if not user.is_authenticated:
        return False

    from allauth.account.models import EmailAddress
    return EmailAddress.objects.filter(user=user, verified=True).exists()


@register.simple_tag(takes_context=True)
def login_url_with_next(context):
    """Generate login URL with the current path as next parameter."""
    request = context.get('request')
    if not request:
        return '/authentication/login/'

    next_url = request.path
    return f'/authentication/login/?next={next_url}'
