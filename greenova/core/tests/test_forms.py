"""Unit tests for core.forms (EnvironmentalObligationForm, CustomUserCreationForm, UserProfileForm).

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
from beartype import beartype
from django.test import TestCase
from greenova.core.forms import (
    EnvironmentalObligationForm,
    CustomUserCreationForm,
    UserProfileForm,
)
from greenova.core.models import CustomUser, UserProfile
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
