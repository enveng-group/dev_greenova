"""Unit tests for core.models (CustomUser, UserProfile, EnvironmentalObligation, AuditLog).

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
from beartype import beartype
from django.test import TestCase
from django.utils import timezone
from greenova.core.models import CustomUser, UserProfile, EnvironmentalObligation, AuditLog


class CustomUserModelTests(TestCase):
    """Tests for the CustomUser model."""

    @beartype
    def test_create_user(self) -> None:
        user = CustomUser.objects.create_user(
            username="alice", email="alice@example.com", password="pass123"
        )
        self.assertEqual(user.username, "alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertFalse(user.is_mfa_enabled)
        self.assertEqual(user.company, "")


class UserProfileModelTests(TestCase):
    """Tests for the UserProfile model."""

    @beartype
    def test_profile_creation(self) -> None:
        user = CustomUser.objects.create_user(
            username="bob", email="bob@example.com", password="pass123"
        )
        profile = UserProfile.objects.create(user=user, display_name="Bobby")
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.display_name, "Bobby")
        self.assertIsInstance(profile.preferences, dict)


class EnvironmentalObligationModelTests(TestCase):
    """Tests for the EnvironmentalObligation model."""

    @beartype
    def test_create_obligation(self) -> None:
        obligation = EnvironmentalObligation.objects.create(
            name="Test Obligation",
            description="Test desc",
            due_date=timezone.now().date(),
        )
        self.assertEqual(obligation.name, "Test Obligation")
        self.assertFalse(obligation.is_complete)
        self.assertIsNotNone(obligation.created_at)
        self.assertIsNotNone(obligation.updated_at)


class AuditLogModelTests(TestCase):
    """Tests for the AuditLog model."""

    @beartype
    def test_create_audit_log(self) -> None:
        user = CustomUser.objects.create_user(
            username="carol", email="carol@example.com", password="pass123"
        )
        log = AuditLog.objects.create(
            user=user,
            action="login",
            object_type="user",
            object_id=str(user.id),
            message="User logged in",
            ip_address="127.0.0.1",
        )
        self.assertEqual(log.user, user)
        self.assertEqual(log.action, "login")
        self.assertEqual(log.object_type, "user")
        self.assertEqual(log.object_id, str(user.id))
        self.assertEqual(log.message, "User logged in")
        self.assertEqual(log.ip_address, "127.0.0.1")
        self.assertIsNotNone(log.timestamp)
