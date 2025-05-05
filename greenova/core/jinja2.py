# Import your custom filters and globals
from django.contrib.staticfiles.storage import staticfiles_storage
from django.middleware.csrf import get_token
from django.urls import reverse
from django.utils import translation
from django_htmx.jinja import django_htmx_script
from django_hyperscript.templatetags.hyperscript import hs_dump
from jinja2 import Environment


def environment(**options):
    """
    Create a custom Jinja2 environment with Django-specific filters and globals.
    """
    # Filter out Django-specific options that Jinja2 doesn't understand
    jinja2_options = {k: v for k, v in options.items()
                      if k not in ['debug']}

    # Set autoescape=True if it's not already specified in options
    if 'autoescape' not in jinja2_options:
        jinja2_options['autoescape'] = True

    # Create environment with filtered options - adding a nosec to satisfy Bandit
    # autoescape is set in jinja2_options above
    env = Environment(**jinja2_options)  # nosec B701
    env.globals['static'] = staticfiles_storage.url
    env.globals['url'] = reverse
    env.globals['get_current_language'] = translation.get_language
    env.globals['csrf_token'] = get_token  # Add CSRF token support
    env.globals['django_htmx_script'] = django_htmx_script  # Add django_htmx support
    env.globals['hyperscript'] = hs_dump  # Using hs_dump instead of hyperscript_widget

    return env
