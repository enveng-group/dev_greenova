"""Unit tests for core.views (profile, audit, etc.).

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
from beartype import beartype
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from core.models import UserProfile

User = get_user_model()


class ProfileViewTests(TestCase):
    """Tests for profile detail and edit views."""

    @beartype
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="frank", email="frank@example.com", password="pass123"
        )
        self.profile = UserProfile.objects.create(user=self.user, display_name="Franky")
        self.client.login(username="frank", password="pass123")

    @beartype
    def test_profile_detail_view(self) -> None:
        url = reverse("core:profile_detail")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.username)

    @beartype
    def test_profile_edit_view_get(self) -> None:
        url = reverse("core:profile_edit")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Edit Profile")

    @beartype
    def test_profile_edit_view_post(self) -> None:
        url = reverse("core:profile_edit")
        response = self.client.post(url, {
            "display_name": "Frank Updated",
            "preferences": "{}",
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.display_name, "Frank Updated")


class ProfileViewTest(TestCase):
    @beartype
    def test_profile_view_authenticated(self) -> None:
        user = User.objects.create_user(
            username="profileview",
            password="testpass",
            email="profileview@example.com")
        UserProfile.objects.create(user=user, display_name="Profile View")
        self.client.login(username="profileview", password="testpass")
        response = self.client.get(reverse("core:profile_detail"))
        self.assertEqual(response.status_code, 200)

    @beartype
    def test_profile_view_unauthenticated(self) -> None:
        response = self.client.get(reverse("core:profile_detail"))
        self.assertNotEqual(response.status_code, 200)


class AuditLogViewTests(TestCase):
    """Tests for the audit log list view."""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="viewuser1",
            email="viewuser1@example.com",
            password="viewpass123!",
        )
        self.client.login(username="viewuser1", password="viewpass123!")

    def test_audit_log_list_view_authenticated(self) -> None:
        response = self.client.get(reverse("core:audit_log_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Audit Log")

    def test_audit_log_list_view_unauthenticated(self) -> None:
        self.client.logout()
        response = self.client.get(reverse("core:audit_log_list"))
        self.assertNotEqual(response.status_code, 200)
