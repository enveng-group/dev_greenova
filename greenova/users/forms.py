# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Forms for user profile and admin user management in the users app.

This module provides Django forms for updating user profiles, managing users
in the admin interface, and uploading profile images.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Forms for user profile, admin user, and profile image upload

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Any, TypeVar

from beartype import beartype
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Fieldset, Layout, Submit
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Model

from .models import Profile
from .types import UserProfileDict, UserPermissionsDict

User = get_user_model()
T = TypeVar("T", bound=Model)


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ["bio", "position", "department", "phone_number", "profile_image"]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    @beartype
    def __init__(
        self,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Initialize the UserProfileForm.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.
        """
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "pk") and self.instance.pk:
            # Type ignore comments prevent type checker errors for user attributes
            # type: ignore
            self.fields["first_name"].initial = self.instance.user.first_name
            # type: ignore
            self.fields["last_name"].initial = self.instance.user.last_name
            self.fields["email"].initial = self.instance.user.email  # type: ignore
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Profile Information",
                "first_name",
                "last_name",
                "email",
                "bio",
                "position",
                "department",
                "phone_number",
                "profile_image",
            ),
            Submit("submit", "Save Profile"),
        )

    @beartype
    def save(self, commit: bool = True) -> Profile:
        """Save the updated profile and related user fields.

        Args:
            commit: Whether to commit changes to the database.

        Returns:
            The updated Profile instance.
        """
        profile = super().save(commit=False)
        user = profile.user  # type: ignore
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()  # type: ignore
            profile.save()
        return profile


class AdminUserForm(forms.ModelForm):
    """Admin form for creating and updating users."""

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=False,
        help_text="Leave blank if you don't want to change the password.",
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    @beartype
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the AdminUserForm.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "User Details",
                "username",
                "email",
                "first_name",
                "last_name",
                "is_active",
                "is_staff",
                "is_superuser",
                "password1",
                "password2",
            ),
            Submit("submit", "Save User"),
        )

    @beartype
    def clean_password1(self) -> str | None:
        """Validate the password1 field using Django's password validators.

        Returns:
            The validated password or None.

        Raises:
            ValidationError: If the password does not meet requirements.
        """
        password = self.cleaned_data.get("password1")
        if password:
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error("password1", error)
        return password

    @beartype
    def clean(self) -> dict[str, Any]:
        """Validate the form, ensuring password fields match.

        Returns:
            The cleaned data dictionary.

        Raises:
            ValidationError: If passwords do not match.
        """
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if (password1 or password2) and password1 != password2:
            self.add_error("password2", "The two password fields didn't match.")

        return cleaned_data

    @beartype
    def save(self, commit: bool = True) -> Any:
        """Save the user instance, setting password if provided.

        Args:
            commit: Whether to commit changes to the database.

        Returns:
            The saved User instance.
        """
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            try:
                validate_password(password, user)  # type: ignore
                user.set_password(password)  # type: ignore
            except ValidationError:
                pass

        if commit:
            user.save()  # type: ignore
        return user


class ProfileImageForm(forms.ModelForm):
    """Form for uploading profile image."""

    class Meta:
        model = Profile
        fields = ["profile_image"]
        widgets = {
            "profile_image": forms.FileInput(attrs={"accept": "image/*"}),
        }

    @beartype
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the ProfileImageForm.

        Args:
            *args: Positional arguments for the parent constructor.
            **kwargs: Keyword arguments for the parent constructor.
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Fieldset(
                "Profile Image",
                "profile_image",
            ),
            Submit("submit", "Upload Image"),
        )
