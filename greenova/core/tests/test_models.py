"""Unit tests for core.models (CustomUser, UserProfile, EnvironmentalObligation, AuditLog).

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
from beartype import beartype
from django.test import TestCase
from django.utils import timezone
from core.models import CustomUser, UserProfile, EnvironmentalObligation, AuditLog


class CustomUserModelTests(TestCase):
    """Tests for the CustomUser model."""

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpass"
        )

    @beartype
    def test_create_user(self) -> None:
        user = CustomUser.objects.create_user(
            username="alice", email="alice@example.com", password="pass123"
        )
        self.assertEqual(user.username, "alice")
        self.assertEqual(user.email, "alice@example.com")
        self.assertFalse(user.is_mfa_enabled)
        self.assertEqual(user.company, "")
        self.assertIsInstance(user, CustomUser)
        self.assertTrue(user.check_password("pass123"))

    def test_user_creation(self) -> None:
        self.assertIsInstance(self.user, CustomUser)
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("testpass"))

    def test_user_str(self) -> None:
        self.assertEqual(str(self.user), self.user.username)


class UserProfileModelTests(TestCase):
    """Tests for the UserProfile model."""

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            username="testuser1",
            email="testuser1@example.com",
            password="testpass123!",
        )
        self.profile = UserProfile.objects.create(
            user=self.user, display_name="Test User")

    @beartype
    def test_profile_creation(self) -> None:
        user = CustomUser.objects.create_user(
            username="bob", email="bob@example.com", password="pass123"
        )
        profile = UserProfile.objects.create(user=user, display_name="Bobby")
        self.assertEqual(profile.user, user)
        self.assertEqual(profile.display_name, "Bobby")
        self.assertIsInstance(profile.preferences, dict)

    @beartype
    def test_create_profile(self) -> None:
        user = CustomUser.objects.create_user(
            username="profileuser",
            password="testpass",
            email="profileuser@example.com")
        profile = UserProfile.objects.create(user=user)
        self.assertEqual(profile.user, user)

    def test_profile_str(self) -> None:
        self.assertEqual(str(self.profile), "Test User")

    def test_profile_user_link(self) -> None:
        self.assertEqual(self.profile.user.username, "testuser1")

    def test_profile_email(self) -> None:
        self.assertEqual(self.profile.user.email, "testuser1@example.com")


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

        obligation_simple = EnvironmentalObligation.objects.create(
            name="Test Obligation",
            description="desc",
            due_date=timezone.now().date(),
        )
        self.assertEqual(obligation_simple.name, "Test Obligation")


class AuditLogModelTests(TestCase):
    """Tests for the AuditLog model."""

    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            username="audituser1",
            email="audituser1@example.com",
            password="auditpass123!",
        )
        self.log = AuditLog.objects.create(
            user=self.user,
            action="login",
            object_type="CustomUser",
            object_id=str(self.user.pk),
            message="User logged in."
        )

    @beartype
    def test_create_audit_log(self) -> None:
        user = CustomUser.objects.create_user(
            username="carol", email="carol@example.com", password="pass123"
        )
        log = AuditLog.objects.create(
            user=user,
            action="login",
            object_type="user",
            object_id=str(user.pk),
            message="User logged in",
            ip_address="127.0.0.1",
        )
        self.assertEqual(log.user, user)
        self.assertEqual(log.action, "login")
        self.assertEqual(log.object_type, "user")
        self.assertEqual(log.object_id, str(user.pk))
        self.assertEqual(log.message, "User logged in")
        self.assertEqual(log.ip_address, "127.0.0.1")
        self.assertIsNotNone(log.timestamp)

        log_simple = AuditLog.objects.create(
            user=user, action="login", timestamp=timezone.now())
        self.assertEqual(log_simple.user, user)
        self.assertEqual(log_simple.action, "login")

    def test_audit_log_str(self) -> None:
        self.assertIn("login", str(self.log))
        self.assertIn("User logged in.", str(self.log))

    def test_audit_log_user(self) -> None:
        self.assertEqual(self.log.user.username, "audituser1")

    def test_audit_log_object_id(self) -> None:
        self.assertEqual(self.log.object_id, str(self.user.pk))
