# Import your custom filters and globals
from dashboard.extensions import dashboard_filters, dashboard_globals
from django.contrib.staticfiles.storage import staticfiles_storage
from django.middleware.csrf import get_token
from django.urls import reverse
from django.utils import translation
from django_htmx.jinja import django_htmx_script
from django_hyperscript.templatetags.hyperscript import hs_dump
from feedback.extensions import feedback_filters, feedback_globals
from jinja2 import Environment
from procedures.extensions import procedure_filters, procedure_globals


def environment(**options):
    """
    Create a custom Jinja2 environment with Django-specific filters and globals.
    """
    # Ensure autoescape is set to True for security
    # and to avoid XSS vulnerabilities.
    env = Environment(autoescape=True, **options)
    env.globals['static'] = staticfiles_storage.url
    env.globals['url'] = reverse
    env.globals['get_current_language'] = translation.get_language
    env.globals['csrf_token'] = get_token  # Add CSRF token support
    env.globals['django_htmx_script'] = django_htmx_script  # Add django_htmx support
    env.globals['hyperscript'] = hs_dump  # Using hs_dump instead of hyperscript_widget

    # Register all procedure filters and globals
    for name, func in procedure_filters.items():
        env.filters[name] = func

    for name, func in procedure_globals.items():
        env.globals[name] = func

    # Register all dashboard filters and globals
    for name, func in dashboard_filters.items():
        env.filters[name] = func

    for name, func in dashboard_globals.items():
        env.globals[name] = func

    # Register all feedback filters and globals
    for name, func in feedback_filters.items():
        env.filters[name] = func

    for name, func in feedback_globals.items():
        env.globals[name] = func

    return env
