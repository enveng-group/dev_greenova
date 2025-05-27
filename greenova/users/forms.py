"""Forms for user and profile management in the Greenova users app.

This module defines forms for updating user profiles, creating and updating users
in the admin, and uploading profile images.
"""
from typing import Any, ClassVar, TypeVar

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Model
from models import Profile

User = get_user_model()
T = TypeVar("T", bound=Model)


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""

    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        """Metadata for UserProfileForm."""
        model = Profile
        fields: ClassVar[list[str]] = [
            "bio",
            "position",
            "department",
            "phone_number",
            "profile_image",
        ]
        widgets: ClassVar[dict[str, Any]] = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Initialize the UserProfileForm and set initial values for user fields."""
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, "pk") and self.instance.pk:
            user = self.instance.user
            self.fields["first_name"].initial = getattr(user, "first_name", "")
            self.fields["last_name"].initial = getattr(user, "last_name", "")
            self.fields["email"].initial = getattr(user, "email", "")

    def save(self, commit: bool = True) -> Profile:
        """Save the profile and update related user fields."""
        profile: Profile = super().save(commit=False)
        user = profile.user
        if hasattr(user, "first_name"):
            setattr(user, "first_name", self.cleaned_data["first_name"])
        if hasattr(user, "last_name"):
            setattr(user, "last_name", self.cleaned_data["last_name"])
        if hasattr(user, "email"):
            setattr(user, "email", self.cleaned_data["email"])

        if commit:
            user.save()
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
        label="Confirm Password", widget=forms.PasswordInput, required=False
    )

    class Meta:
        """Metadata for AdminUserForm."""
        model = User
        fields: ClassVar[list[str]] = [
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "is_superuser",
        ]

    def clean_password1(self) -> str | None:
        """Validate the first password field using Django's password validation."""
        password = self.cleaned_data.get("password1")
        if password:
            # Validate password against Django's password validation rules
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                # Pass the errors to the form
                self.add_error("password1", error)
        return password

    def clean(self) -> dict[str, Any]:
        """Clean and validate the form data, ensuring password fields match."""
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", "The two password fields didn't match.")

        return cleaned_data

    def save(self, commit: bool = True) -> Any:
        """Save the user instance, setting the password if provided."""
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")

        if password:
            try:
                validate_password(password, user)
                user.set_password(password)
            except ValidationError:
                pass

        if commit:
            user.save()
        return user


class ProfileImageForm(forms.ModelForm):
    """Form for uploading profile image."""

    class Meta:
        """Metadata for ProfileImageForm."""
        model = Profile
        fields: ClassVar[list[str]] = ["profile_image"]
        widgets: ClassVar[dict[str, Any]] = {
            "profile_image": forms.FileInput(
                attrs={"accept": "image/*"}
            )
        }
