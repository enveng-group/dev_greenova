"""
Type definitions for the Greenova project.
"""
from django.http import HttpRequest as HttpRequestBase
from django_htmx.middleware import HtmxDetails

class HttpRequest(HttpRequestBase):
    """
    Enhanced HttpRequest class with HTMX support.

    This type definition helps static type checkers understand that
    request.htmx is available when using django-htmx middleware.
    """
    htmx: HtmxDetails
