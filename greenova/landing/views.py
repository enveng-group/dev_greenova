"""Views for the Greenova landing app.

All API endpoints in this app use Protobuf3 for serialization and deserialization.
Newsletter signup and landing page content are exchanged as Protobuf3-encoded messages.
See landing/serializers.py for details.
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License: AGPL-3.0

import logging

import bleach
from beartype import beartype
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

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
@require_http_methods(["POST", "GET"])
@beartype
def newsletter_signup(request: HttpRequest) -> HttpResponse:
    """Handle newsletter signup form submission.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Redirect or re-render with form errors.

    """
    if request.method == "POST":
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            email: str = bleach.clean(form.cleaned_data["email"], strip=True)
            # Here you would add logic to save the email to a newsletter list or send
            # to an API
            logger.info("Newsletter signup: %s", email)
            messages.success(request, "Thank you for subscribing!")
            return redirect(reverse("landing:home"))
        logger.warning("Newsletter signup form invalid: %s", form.errors)
    else:
        form = NewsletterSignupForm()
    html = render_to_string("landing/landing.html", {"form": form}, request=request)
    return HttpResponse(html)


@beartype
def landing_page_api(request: HttpRequest) -> HttpResponse:
    """API endpoint to serve landing page content as Protobuf.

    This view demonstrates the use of Protobuf serialization for landing page
    content, which can be consumed by frontend applications or external services.

    Args:
        request: The HTTP request object.

    Returns:
        HttpResponse: Protobuf-serialized landing page content.

    """
    try:
        hero_title: str = "Transform Your Environmental Management"
        hero_subtitle: str = (
            "Streamline compliance tracking with Greenova's powerful platform"
        )
        features: list[dict[str,
                            str]] = [{"title": "Compliance Tracking",
                                      "description": "Monitor all your environmental obligations in one place",
                                      },
                                     {"title": "Automated Alerts",
                                      "description": "Never miss a deadline with smart notification system",
                                      },
                                     {"title": "Detailed Reporting",
                                      "description": "Generate comprehensive compliance reports instantly",
                                      },
                                     ]
        stats: dict[str, int] = {
            "Active Organizations": 150,
            "Tracked Obligations": 2500,
            "Compliance Rate": 98,
        }
        benefits: list[str] = [
            "Reduce compliance risks",
            "Save time on manual tracking",
            "Improve environmental performance",
            "Streamline reporting processes",
        ]
        testimonials: list[dict[str,
                                str]] = [{"name": "Sarah Chen",
                                          "content": "Greenova has revolutionized how we manage our environmental compliance.",
                                          },
                                         {"name": "Marcus Johnson",
                                          "content": "The analytics capabilities in Greenova have given us unprecedented insights.",
                                          },
                                         {"name": "Elena Rodriguez",
                                          "content": "The regulatory updates feature in Greenova keeps us ahead of changing requirements.",
                                          },
                                         ]
        cta_title: str = "Ready to Transform Your Environmental Compliance?"
        cta_subtitle: str = "Join thousands of environmental professionals who have simplified their compliance management with Greenova."
        data: bytes = LandingSerializer.serialize_landing_page_content(
            hero_title=hero_title,
            hero_subtitle=hero_subtitle,
            features=features,
            stats=stats,
            benefits=benefits,
            testimonials=testimonials,
            cta_title=cta_title,
            cta_subtitle=cta_subtitle,
        )
        logger.info("Landing page API served protobuf content")
        return HttpResponse(data, content_type="application/x-protobuf")
    except Exception as e:
        logger.exception("Failed to serve landing page API: %s", e)
        return JsonResponse(
            {"error": "Failed to generate landing page content"}, status=500
        )
