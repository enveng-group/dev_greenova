"""Unit tests for the Greenova landing app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

"""Tests for the landing app."""

from beartype import beartype
import pytest
from django.test import TestCase
from django.urls import reverse
from django.utils.html import escape
from .serializers import LandingSerializer
from .forms import NewsletterSignupForm


class LandingPageTests(TestCase):
    """Test landing page view and template rendering."""

    @beartype
    def test_landing_page(self) -> None:
        """Landing page returns 200 and uses correct template."""
        response = self.client.get(reverse("landing:home"))
        assert response.status_code == 200
        self.assertTemplateUsed(response, "landing/landing.html")
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


class LandingSerializerTests(TestCase):
    """Test LandingSerializer protobuf serialization/deserialization."""

    @beartype
    def test_serialize_and_deserialize_newsletter_signup_request(self) -> None:
        email = "test@example.com"
        data = LandingSerializer.serialize_newsletter_signup_request(email)
        result = LandingSerializer.deserialize_newsletter_signup_request(data)
        assert result == email

    @beartype
    def test_serialize_newsletter_signup_request_invalid_email(self) -> None:
        with pytest.raises(Exception):
            LandingSerializer.serialize_newsletter_signup_request("not-an-email")

    @beartype
    def test_serialize_and_deserialize_newsletter_signup_response(self) -> None:
        data = LandingSerializer.serialize_newsletter_signup_response(True, "Success")
        result = LandingSerializer.deserialize_newsletter_signup_response(data)
        assert result["success"] is True
        assert result["message"] == "Success"

    @beartype
    def test_serialize_and_deserialize_landing_page_content(self) -> None:
        features = [
            {"title": "Feature 1", "description": "Desc 1"},
            {"title": "Feature 2", "description": "Desc 2"},
        ]
        stats = {"Completed": 10, "Pending": 5}
        benefits = ["Benefit 1", "Benefit 2"]
        testimonials = [
            {"name": "Alice", "content": "Great!"},
            {"name": "Bob", "content": "Excellent!"},
        ]
        data = LandingSerializer.serialize_landing_page_content(
            hero_title="Hero Title",
            hero_subtitle="Hero Subtitle",
            features=features,
            stats=stats,
            benefits=benefits,
            testimonials=testimonials,
            cta_title="CTA Title",
            cta_subtitle="CTA Subtitle",
        )
        result = LandingSerializer.deserialize_landing_page_content(data)
        assert result["hero_title"] == "Hero Title"
        assert result["features"][0]["title"] == "Feature 1"
        assert result["stats"]["Completed"] == 10
        assert result["benefits"] == benefits
        assert result["testimonials"][0]["name"] == "Alice"
        assert result["cta_title"] == "CTA Title"

    @beartype
    def test_deserialize_newsletter_signup_request_invalid(self) -> None:
        with pytest.raises(Exception):
            LandingSerializer.deserialize_newsletter_signup_request(b"not-protobuf")

    @beartype
    def test_deserialize_newsletter_signup_response_invalid(self) -> None:
        with pytest.raises(Exception):
            LandingSerializer.deserialize_newsletter_signup_response(b"not-protobuf")

    @beartype
    def test_deserialize_landing_page_content_invalid(self) -> None:
        with pytest.raises(Exception):
            LandingSerializer.deserialize_landing_page_content(b"not-protobuf")
