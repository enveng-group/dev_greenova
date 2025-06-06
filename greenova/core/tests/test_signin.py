"""Tests for the Greenova sign-in flow using django-allauth.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
from beartype import beartype
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class SignInFlowTests(TestCase):
    """Test the sign-in flow using django-allauth."""

    @beartype
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpass123"
        )

    @beartype
    def test_login_page_loads(self) -> None:
        url = reverse("account_login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign In")

    @beartype
    def test_login_success(self) -> None:
        url = reverse("account_login")
        response = self.client.post(url, {
            "login": "testuser",
            "password": "testpass123"
        }, follow=True)
        self.assertTrue(response.context["user"].is_authenticated)

    @beartype
    def test_login_failure(self) -> None:
        url = reverse("account_login")
        response = self.client.post(url, {
            "login": "testuser",
            "password": "wrongpass"
        })
        self.assertFalse(response.context["user"].is_authenticated)
        self.assertContains(response, "Sign In")
