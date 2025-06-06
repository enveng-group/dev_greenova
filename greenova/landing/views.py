"""Views for the Greenova landing app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

import logging

import bleach
from beartype import beartype
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse

from .forms import NewsletterSignupForm

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
    context = {
        "form": form,
        "context": {},  # for bootstrap_messages
    }
    html = render_to_string(
        "landing/landing.html",
        context,
        request=request,
    )
    return HttpResponse(html)


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
            email = bleach.clean(form.cleaned_data["email"])
            # TODO(Adrian Gallo): Save email to newsletter list or send to external service
            # See issue: https://github.com/enveng-group/greenova/issues/1
            logger.info("Newsletter signup: %s", email)
            messages.success(request, "Thank you for subscribing!")
            return redirect(reverse("landing:home"))
        logger.warning("Newsletter signup form invalid: %s", form.errors)
    else:
        form = NewsletterSignupForm()
    html = render_to_string("landing/landing.html", {"form": form}, request=request)
    return HttpResponse(html)
