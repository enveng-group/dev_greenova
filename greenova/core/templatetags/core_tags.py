<<<<<<< HEAD
import logging

from core.commons import get_active_namespace, get_user_display_name
from core.constants import AUTH_NAVIGATION, MAIN_NAVIGATION, USER_NAVIGATION
from django import template
from django.conf import settings
from django.urls import NoReverseMatch, reverse
=======
from django import template
from django.urls import reverse, NoReverseMatch
from django.utils.html import format_html
from django.conf import settings
from typing import Dict, List, Optional, Union
import logging

from core.constants import MAIN_NAVIGATION, USER_NAVIGATION, AUTH_NAVIGATION, THEME_OPTIONS
from core.commons import get_active_namespace, get_user_display_name
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

logger = logging.getLogger(__name__)
register = template.Library()

<<<<<<< HEAD

@register.simple_tag(takes_context=True)
def active_link(context, url_name, css_class='active'):
    """Return css_class if the current URL matches the given URL name."""
    request = context.get('request')
    if not request:
        return ''
=======
@register.simple_tag(takes_context=True)
def active_link(context, url_name, css_class="active"):
    """Return css_class if the current URL matches the given URL name."""
    request = context.get('request')
    if not request:
        return ""
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

    try:
        current_url = request.path
        target_url = reverse(url_name)
        if current_url.startswith(target_url):
            return css_class
    except NoReverseMatch:
<<<<<<< HEAD
        logger.debug('No reverse match for %s', url_name)  # Fixed lazy formatting
    return ''

=======
        logger.debug(f"No reverse match for {url_name}")
    return ""
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

@register.inclusion_tag('core/components/breadcrumbs.html', takes_context=True)
def breadcrumb_navigation(context):
    """Render breadcrumb navigation based on request path."""
    request = context.get('request')
    if not request:
        return {'crumbs': []}

    # Build breadcrumbs based on namespace and url name
    crumbs = []

    # Always include home
<<<<<<< HEAD
    crumbs.append(
        {
            'title': 'Home',
            'url': reverse('home'),
            'active': request.path == reverse('home'),
        }
    )
=======
    crumbs.append({
        'title': 'Home',
        'url': reverse('home'),
        'active': request.path == reverse('home'),
    })
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

    # Add namespace-based breadcrumb if applicable
    namespace = get_active_namespace(request)
    if namespace and namespace != 'home':
        try:
            url = reverse(f'{namespace}:home')
<<<<<<< HEAD
            crumbs.append(
                {
                    'title': namespace.title(),
                    'url': url,
                    'active': request.path == url,
                }
            )
=======
            crumbs.append({
                'title': namespace.title(),
                'url': url,
                'active': request.path == url,
            })
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
        except NoReverseMatch:
            # Try with just the namespace
            try:
                url = reverse(namespace)
<<<<<<< HEAD
                crumbs.append(
                    {
                        'title': namespace.title(),
                        'url': url,
                        'active': request.path == url,
                    }
                )
            except NoReverseMatch:
                # Just add the namespace as text
                crumbs.append(
                    {
                        'title': namespace.title(),
                        'url': None,
                        'active': True,
                    }
                )

    return {'crumbs': crumbs}


=======
                crumbs.append({
                    'title': namespace.title(),
                    'url': url,
                    'active': request.path == url,
                })
            except NoReverseMatch:
                # Just add the namespace as text
                crumbs.append({
                    'title': namespace.title(),
                    'url': None,
                    'active': True,
                })

    return {'crumbs': crumbs}

>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
@register.inclusion_tag('core/components/auth_menu.html', takes_context=True)
def auth_menu(context):
    """Render authentication menu based on user status."""
    request = context.get('request')
    user = request.user if request else None

    return {
<<<<<<< HEAD
        'is_authenticated': user.is_authenticated if user else False,
        'user_display_name': (
            get_user_display_name(user) if user and user.is_authenticated else ''
        ),
        'user_navigation': USER_NAVIGATION,
        'auth_navigation': AUTH_NAVIGATION,
    }


@register.inclusion_tag('core/components/theme_switcher.html')
def theme_switcher():
    """
    Renders theme switcher with available theme options.
    """
    theme_options = [
        ('Auto', 'auto'),
        ('Light', 'light'),
        ('Dark', 'dark'),
    ]
    return {'theme_options': theme_options}

=======
        'user': user,
        'is_authenticated': user.is_authenticated if user else False,
        'user_navigation': USER_NAVIGATION,
        'auth_navigation': AUTH_NAVIGATION,
        'user_display_name': get_user_display_name(user) if user and user.is_authenticated else None,
    }

@register.inclusion_tag('core/components/theme_switcher.html')
def theme_switcher():
    """Render theme switcher component."""
    return {
        'theme_options': THEME_OPTIONS,
    }
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))

@register.simple_tag
def site_version():
    """Return the current site version."""
    return getattr(settings, 'APP_VERSION', 'dev')

<<<<<<< HEAD

=======
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
@register.inclusion_tag('core/components/main_navigation.html', takes_context=True)
def main_navigation(context):
    """Render the main navigation menu."""
    request = context.get('request')
    current_namespace = get_active_namespace(request) if request else ''

    return {
        'navigation_items': MAIN_NAVIGATION,
        'current_namespace': current_namespace,
    }

<<<<<<< HEAD

=======
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
@register.filter
def user_role_in_project(project, user):
    """Get user's role in a project."""
    if hasattr(project, 'get_user_role'):
        return project.get_user_role(user)
    return None

<<<<<<< HEAD

=======
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
@register.simple_tag(takes_context=True)
def base_url(context):
    """Get the base URL from the request."""
    request = context.get('request')
    if request:
<<<<<<< HEAD
        return f'{request.scheme}://{request.get_host()}'
    return ''
=======
        return f"{request.scheme}://{request.get_host()}"
    return ""
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
