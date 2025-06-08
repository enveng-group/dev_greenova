"""Unit tests for core.forms (EnvironmentalObligationForm, CustomUserCreationForm, UserProfileForm, UserCreationForm).

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
from beartype import beartype
from django.test import TestCase
from core.forms import (
    EnvironmentalObligationForm,
    CustomUserCreationForm,
    UserProfileForm,
)
from core.models import CustomUser, UserProfile
from django.utils import timezone


class EnvironmentalObligationFormTests(TestCase):
    """Tests for EnvironmentalObligationForm."""

    @beartype
    def test_valid_form(self) -> None:
        form = EnvironmentalObligationForm(data={
            "name": "Test Obligation",
            "description": "Test desc",
            "due_date": timezone.now().date(),
            "is_complete": False,
        })
        self.assertTrue(form.is_valid())

    @beartype
    def test_partial_form(self) -> None:
        form = EnvironmentalObligationForm(data={
            "name": "Test",
            "description": "desc",
            "due_date": timezone.now().date(),
        })
        self.assertTrue(form.is_valid())


class CustomUserCreationFormTests(TestCase):
    """Tests for CustomUserCreationForm."""

    @beartype
    def test_valid_user_creation(self) -> None:
        form = CustomUserCreationForm(data={
            "username": "dave",
            "email": "dave@example.com",
            "password1": "pass12345",
            "password2": "pass12345",
            "company": "EnvEng",
            "is_mfa_enabled": True,
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.username, "dave")
        self.assertEqual(user.email, "dave@example.com")
        self.assertTrue(user.is_mfa_enabled)
        self.assertEqual(user.company, "EnvEng")

    @beartype
    def test_minimal_user_creation(self) -> None:
        form = CustomUserCreationForm(data={
            "username": "newuser",
            "email": "newuser_minimal2@example.com",
            "password1": "aS3cureP@ssw0rd!",
            "password2": "aS3cureP@ssw0rd!",
            "company": "",
            "is_mfa_enabled": False,
        })
        self.assertTrue(form.is_valid())

    def test_password_mismatch(self) -> None:
        form_data = {
            "username": "newuser2",
            "email": "newuser2@example.com",
            "password1": "StrongPass123!",
            "password2": "WrongPass123!",
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserProfileFormTests(TestCase):
    """Tests for UserProfileForm."""

    @beartype
    def test_valid_profile_form(self) -> None:
        user = CustomUser.objects.create_user(
            username="eve", email="eve@example.com", password="pass123"
        )
        profile = UserProfile.objects.create(user=user)
        form = UserProfileForm(data={
            "display_name": "Evie",
            "preferences": "{}",
        }, instance=profile)
        self.assertTrue(form.is_valid())

    @beartype
    def test_minimal_profile_form(self) -> None:
        user = CustomUser.objects.create_user(
            username="profileform", password="testpass", email="profileform@example.com"
        )
        profile = UserProfile.objects.create(user=user)
        form = UserProfileForm(data={}, instance=profile)
        self.assertTrue(form.is_valid())

    def test_valid_form(self) -> None:
        form_data = {
            "display_name": "Test User",
            "bio": "Test bio.",
        }
        form = UserProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self) -> None:
        form_data = {"display_name": ""}  # Required field missing
        form = UserProfileForm(data=form_data)
        self.assertFalse(form.is_valid())


class UserCreationFormTest(TestCase):
    """Tests for UserCreationForm."""

    def test_valid_form(self) -> None:
        form = CustomUserCreationForm(data={
            "username": "testuser2",
            "email": "testuser2@example.com",
            "password1": "testpass123",
            "password2": "testpass123",
        })
        self.assertTrue(form.is_valid())

    def test_invalid_form(self) -> None:
        form = CustomUserCreationForm(data={
            "username": "",
            "email": "not-an-email",
            "password1": "123",
            "password2": "456",
        })
        self.assertFalse(form.is_valid())
