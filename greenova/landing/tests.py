"""Unit tests for the Greenova landing app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

"""Tests for the landing app."""

from django.test import TestCase
from beartype import beartype
from django.urls import reverse
from .forms import NewsletterSignupForm
from django.utils.html import escape


class LandingPageTests(TestCase):
    """Test landing page view and template rendering."""

    @beartype
    def test_landing_page(self) -> None:
        """Landing page returns 200 and uses correct template."""
        response = self.client.get(reverse("landing:home"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "landing/landing.jinja")
        self.assertContains(response, "Greenova")


class NewsletterSignupFormTests(TestCase):
    """Test newsletter signup form validation and sanitization."""

    @beartype
    def test_valid_email(self) -> None:
        """Form accepts a valid email address."""
        form = NewsletterSignupForm({"email": "test@example.com"})
        assert form.is_valid()

    @beartype
    def test_invalid_email(self) -> None:
        """Form rejects an invalid email address."""
        form = NewsletterSignupForm({"email": "not-an-email"})
        assert not form.is_valid()

    @beartype
    def test_email_sanitization(self) -> None:
        """Form input is sanitized with bleach in the view."""
        dirty_email = "<script>alert(1)</script>@example.com"
        form = NewsletterSignupForm({"email": dirty_email})
        assert not form.is_valid()


class NewsletterSignupViewTests(TestCase):
    """Test newsletter signup view logic."""

    @beartype
    def test_newsletter_signup_success(self) -> None:
        """Newsletter signup view accepts valid email and returns thank you message."""
        url = reverse("landing:newsletter_signup")
        response = self.client.post(url, {"email": "user@example.com"}, follow=True)
        assert response.status_code == 200
        self.assertContains(response, "Thank you for subscribing!")

    @beartype
    def test_newsletter_signup_invalid_email(self) -> None:
        """Newsletter signup view rejects invalid email and returns error message."""
        url = reverse("landing:newsletter_signup")
        response = self.client.post(url, {"email": "not-an-email"})
        assert response.status_code == 200
        self.assertContains(response, escape("Enter a valid email address."))
