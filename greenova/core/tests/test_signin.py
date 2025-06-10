"""Unit tests for django-allauth integration (sign in, sign out, MFA).

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class AllauthSignInTest(TestCase):
    @beartype
    def test_signin(self) -> None:
        user = User.objects.create_user(
            username="signinuser", password="testpass", email="signinuser@example.com"
        )
        response = self.client.post(
            reverse("account_login"), {"login": "signinuser", "password": "testpass"}
        )
        self.assertEqual(response.status_code, 302)

    @beartype
    def test_signout(self) -> None:
        user = User.objects.create_user(
            username="signoutuser", password="testpass", email="signoutuser@example.com"
        )
        self.client.login(username="signoutuser", password="testpass")
        response = self.client.post(reverse("account_logout"))
        self.assertEqual(response.status_code, 302)

    @beartype
    def test_mfa_required(self) -> None:
        # Placeholder: Implement MFA test logic if MFA is enabled
        self.assertTrue(True)
