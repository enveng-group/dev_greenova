"""Views for the landing page of the Greenova application.

This module contains the main landing page view and related utilities, such as
handling newsletter signups.
"""

import logging
import smtplib
from smtplib import SMTPException
from typing import Any, TypedDict

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.views.decorators.vary import vary_on_headers
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)


# Type definition for django-htmx request attribute
class HtmxDetails(TypedDict, total=False):
    """Type hints for django-htmx request.htmx attributes."""

    boosted: bool
    current_url: str
    history_restore_request: bool
    prompt: str
    target: str
    trigger: str
    trigger_name: str


@method_decorator(
    cache_control(private=True, no_cache=True, no_store=True, must_revalidate=True),
    name="dispatch",
)
@method_decorator(vary_on_headers("HX-Request"), name="dispatch")
class HomeView(TemplateView):
    """Landing page view that handles both regular and HTMX requests."""

    template_name = "landing/index.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        """Handle GET requests for the landing page."""
        logger.debug(
            "Landing page - User authenticated: %s, Post-logout: %s",
            request.user.is_authenticated,
            getattr(request, "is_post_logout", False),
        )

        # If user is authenticated, redirect to dashboard unless post-logout
        if request.user.is_authenticated and not getattr(
            request, "is_post_logout", False
        ):
            logger.debug("Redirecting authenticated user to dashboard")
            return redirect("/dashboard/")

        # Get standard response
        response = super().get(request, *args, **kwargs)

        # Ensure proper cache control
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response["Pragma"] = "no-cache"
        response["Expires"] = "0"

        # Handle HTMX-specific behavior
        if getattr(request, "htmx", None):
            # Set HX-Push-Url header directly
            response["HX-Push-Url"] = request.path

            # Check for forced refresh after logout
            if request.session.pop("_force_refresh", False):
                # Return a response with HX-Refresh header
                refresh_response = HttpResponse()
                refresh_response["HX-Refresh"] = "true"
                return refresh_response

        return response

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add landing page context data."""
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "app_version": getattr(settings, "APP_VERSION", "0.1.0"),
                "show_landing_content": True,
                "show_dashboard_link": self.request.user.is_authenticated,
                "is_post_logout": getattr(self.request, "is_post_logout", False),
            }
        )
        return context


@require_POST
@csrf_protect
def newsletter_signup(request: HttpRequest) -> HttpResponse:
    """Handle newsletter signup form submissions from the landing page.

    Args:
        request: The HTTP request containing email data

    Returns:
        JSON response with success/error message
    """
    email = request.POST.get("email")

    # Validate email
    if not email:
        logger.warning("Newsletter signup attempt with empty email")
        return JsonResponse({"success": False, "message": "Email address is required."})

    try:
        # Simulate sending an email as a placeholder for newsletter integration
        smtp = smtplib.SMTP("localhost")
        smtp.sendmail("no-reply@greenova.com", email, "Welcome to Greenova!")
        smtp.quit()

        # Return success response for HTMX to update the DOM
        return render(
            request,
            "landing/partials/newsletter_success.html",
            {
                "email": email,
            },
        )
    except SMTPException as e:
        logger.error("SMTP error during newsletter signup: %s", str(e))
        return render(request, "landing/partials/newsletter_error.html")
