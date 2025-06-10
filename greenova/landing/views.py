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
    """Render the Greenova landing page with Protobuf3 content.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: The rendered landing page.

    """
    logger.info("Rendering landing page")
    form = NewsletterSignupForm()
    # Get landing page content from serializer (Protobuf3)
    data = LandingSerializer.serialize_landing_page_content(hero_title="Greenova Environmental Management",
                                                            hero_subtitle="Simplify compliance. Empower sustainability. Trusted by professionals across industries.",
                                                            features=[{"title": "Automated Compliance Tracking",
                                                                       "description": "Monitor obligations and deadlines with real-time alerts.",
                                                                       },
                                                                      {"title": "Centralized Documentation",
                                                                       "description": "All your compliance evidence and records in one place.",
                                                                       },
                                                                      {"title": "Powerful Reporting",
                                                                       "description": "Generate audit-ready reports in seconds.",
                                                                       },
                                                                      ],
                                                            stats={"Active Users": 1200,
                                                                   "Projects Managed": 85,
                                                                   "Obligations Tracked": 3400,
                                                                   "Compliance Rate": 98,
                                                                   },
                                                            benefits=["Reduce audit risk and manual effort",
                                                                      "Stay ahead of regulatory changes",
                                                                      "Empower your team with collaboration tools",
                                                                      ],
                                                            testimonials=[{"name": "Jane Smith, EnviroCorp",
                                                                           "content": "Greenova transformed our compliance process.",
                                                                           },
                                                                          {"name": "John Doe, EcoConsult",
                                                                           "content": "The best tool for environmental professionals.",
                                                                           },
                                                                          ],
                                                            cta_title="Ready to Transform Your Environmental Compliance?",
                                                            cta_subtitle="Join thousands of environmental professionals who have simplified their compliance management with Greenova.",
                                                            )
    content = LandingSerializer.deserialize_landing_page_content(data)
    context: dict[str, object] = {
        "form": form,
        **content,
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
    """Handle newsletter signup form submission with Protobuf3 serialization.

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
            logger.info("Newsletter signup: %s", email)
            # Serialize request and response using Protobuf3
            LandingSerializer.serialize_newsletter_signup_request(email)
            # (Here you would save req_bytes to a queue or service)
            resp_bytes = LandingSerializer.serialize_newsletter_signup_response(
                True, "Thank you for signing up!"
            )
            if request.headers.get("Content-Type") == "application/x-protobuf":
                return HttpResponse(resp_bytes, content_type="application/x-protobuf")
            messages.success(
                request, "Thank you for signing up for the Greenova newsletter!"
            )
            return redirect("landing:home")
        logger.warning("Newsletter signup failed: %s", form.errors)
        resp_bytes = LandingSerializer.serialize_newsletter_signup_response(
            False, "Invalid email address."
        )
        if request.headers.get("Content-Type") == "application/x-protobuf":
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
