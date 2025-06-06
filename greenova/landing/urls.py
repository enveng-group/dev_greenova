"""URL configuration for the Greenova landing app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from django.urls import path

from .views import landing_page, newsletter_signup

app_name = "landing"

urlpatterns = [
    path("", landing_page, name="home"),
    path("newsletter_signup", newsletter_signup, name="newsletter_signup"),
]
