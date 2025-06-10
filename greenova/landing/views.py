"""Views for the Greenova landing app.

All API endpoints in this app use Protobuf3 for serialization and deserialization.
Newsletter signup and landing page content are exchanged as Protobuf3-encoded messages.
See landing/serializers.py for details.
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License: AGPL-3.0

import logging

from beartype import beartype
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_http_methods

from .forms import NewsletterSignupForm
from .serializers import LandingSerializer

logger = logging.getLogger(__name__)


@beartype
def landing_page(request: HttpRequest) -> HttpResponse:
    """Render the Greenova landing page.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered landing page.

    """
    logger.info("Rendering landing page")
    form = NewsletterSignupForm()
    context: dict[str, object] = {
        "form": form,
        "context": {},  # for bootstrap_messages
    }
    html = render_to_string(
        "landing/landing.html",
        context,
        request=request,
    )
    return HttpResponse(html)


@csrf_protect
@require_http_methods(["GET", "POST"])
@beartype
def newsletter_signup(request: HttpRequest) -> HttpResponse:
    """Handle newsletter signup form submission.

    Accepts GET (renders form) and POST (validates and processes signup).
    Uses Protobuf3 for API serialization if request is AJAX or content-type is protobuf.

    Args:
        request: Django HttpRequest object.

    Returns:
        HttpResponse with form or result message.

    """
    if request.method == "POST":
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            # Here you would add logic to save the email to a newsletter list or send
            # to a service
            logger.info("Newsletter signup: %s", email)
            if request.headers.get("Content-Type") == "application/x-protobuf":
                resp_bytes = LandingSerializer.build_newsletter_signup_response(
                    True, "Thank you for signing up!"
                )
                return HttpResponse(resp_bytes, content_type="application/x-protobuf")
            messages.success(
                request, "Thank you for signing up for the Greenova newsletter!"
            )
            return redirect("landing:home")
        logger.warning("Newsletter signup failed: %s", form.errors)
        if request.headers.get("Content-Type") == "application/x-protobuf":
            resp_bytes = LandingSerializer.build_newsletter_signup_response(
                False, "Invalid email address."
            )
            return HttpResponse(resp_bytes, content_type="application/x-protobuf")
    else:
        form = NewsletterSignupForm()
    return render(request, "landing/sections/newsletter_form.html", {"form": form})


@require_GET
@beartype
def landing_page_api(request: HttpRequest) -> HttpResponse:
    """API endpoint to serve landing page content as Protobuf3.

    Returns:
        HttpResponse with Protobuf-encoded LandingPageContent.

    """
    data = LandingSerializer.build_landing_page_content()
    return HttpResponse(data, content_type="application/x-protobuf")
