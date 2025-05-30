"""URL configuration for the landing app.

Defines URL patterns for the landing page and newsletter signup.
"""

# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

# Standard library imports
# ...none...

# Third-party imports
from django.urls import path

# Local application imports
from landing.views import HomeView, newsletter_signup

app_name = "landing"

urlpatterns = [
    path("", HomeView.as_view(), name="index"),
    path("newsletter-signup/", newsletter_signup, name="newsletter_signup"),
]
