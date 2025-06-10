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
from .forms import NewsletterSignupForm
from greenova.landing import landing_pb2


class LandingPageTests(TestCase):
    """Test landing page view and template rendering."""

    @beartype
    def test_landing_page(self) -> None:
        url = reverse("landing:home")
        response = self.client.get(url)
        assert response.status_code == 200
        assert b"Welcome to Greenova" in response.content
        assert b"Start Free Trial" in response.content
        assert b"Sign In" in response.content


class NewsletterSignupFormTests(TestCase):
    """Test newsletter signup form validation and sanitization."""

    @beartype
    def test_valid_email(self) -> None:
        form = NewsletterSignupForm({"email": "TestUser@Example.com "})
        assert form.is_valid()
        assert form.cleaned_data["email"] == "testuser@example.com"

    @beartype
    def test_invalid_email(self) -> None:
        form = NewsletterSignupForm({"email": "not-an-email"})
        assert not form.is_valid()
        assert "email" in form.errors

    @beartype
    def test_email_sanitization(self) -> None:
        form = NewsletterSignupForm({"email": "  USER@DOMAIN.COM  "})
        assert form.is_valid()
        assert form.cleaned_data["email"] == "user@domain.com"


class NewsletterSignupViewTests(TestCase):
    """Test newsletter signup view logic."""

    @beartype
    def test_newsletter_signup_success(self) -> None:
        url = reverse("landing:newsletter_signup")
        response = self.client.post(url, {"email": "valid@example.com"}, follow=True)
        assert response.status_code == 200
        assert b"Thank you for signing up" in response.content

    @beartype
    def test_newsletter_signup_invalid_email(self) -> None:
        url = reverse("landing:newsletter_signup")
        response = self.client.post(url, {"email": "bad-email"}, follow=True)
        assert response.status_code == 200
        assert b"email" in response.content


class LandingSerializerTests(TestCase):
    """Test LandingSerializer protobuf serialization/deserialization."""

    @beartype
    def test_serialize_and_deserialize_newsletter_signup_request(self) -> None:
        email = "test@example.com"
        req = landing_pb2.NewsletterSignupRequest(email=email)
        data = req.SerializeToString()
        parsed = landing_pb2.NewsletterSignupRequest()
        parsed.ParseFromString(data)
        assert parsed.email == email

    @beartype
    def test_serialize_newsletter_signup_request_invalid_email(self) -> None:
        # Protobuf does not validate email format, so this should succeed
        email = "not-an-email"
        req = landing_pb2.NewsletterSignupRequest(email=email)
        data = req.SerializeToString()
        parsed = landing_pb2.NewsletterSignupRequest()
        parsed.ParseFromString(data)
        assert parsed.email == email

    @beartype
    def test_serialize_and_deserialize_newsletter_signup_response(self) -> None:
        resp = landing_pb2.NewsletterSignupResponse(success=True, message="OK")
        data = resp.SerializeToString()
        parsed = landing_pb2.NewsletterSignupResponse()
        parsed.ParseFromString(data)
        assert parsed.success
        assert parsed.message == "OK"

    @beartype
    def test_serialize_and_deserialize_landing_page_content(self) -> None:
        content = landing_pb2.LandingPageContent(
            hero_title="Hero Title",
            hero_subtitle="Hero Subtitle",
            features=[landing_pb2.Feature(title="F1", description="D1")],
            stats=[landing_pb2.Stat(name="S1", value=1)],
            benefits=["Benefit 1"],
            testimonials=[landing_pb2.Testimonial(name="T1", content="C1")],
            cta_title="CTA Title",
            cta_subtitle="CTA Subtitle",
        )
        data = content.SerializeToString()
        parsed = landing_pb2.LandingPageContent()
        parsed.ParseFromString(data)
        assert parsed.hero_title == "Hero Title"
        assert parsed.features[0].title == "F1"
        assert parsed.stats[0].name == "S1"
        assert parsed.benefits[0] == "Benefit 1"
        assert parsed.testimonials[0].name == "T1"
        assert parsed.cta_title == "CTA Title"
        assert parsed.cta_subtitle == "CTA Subtitle"

    @beartype
    def test_deserialize_newsletter_signup_request_invalid(self) -> None:
        # Invalid data should raise DecodeError
        with pytest.raises(Exception):
            data = b"not-protobuf"
            parsed = landing_pb2.NewsletterSignupRequest()
            parsed.ParseFromString(data)
