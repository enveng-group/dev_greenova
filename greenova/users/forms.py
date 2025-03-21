from typing import Any, Dict, Optional, TypeVar

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db.models import Model

from .models import Profile

User = get_user_model()
T = TypeVar('T', bound=Model)


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = Profile
        fields = ['bio', 'position', 'department', 'phone_number', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(
        self,
        *args: Any,
        **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'pk') and self.instance.pk:
            # Type ignore comments prevent type checker errors for user attributes
            self.fields['first_name'].initial = self.instance.user.first_name  # type: ignore
            self.fields['last_name'].initial = self.instance.user.last_name  # type: ignore
            self.fields['email'].initial = self.instance.user.email  # type: ignore

    def save(self, commit: bool = True) -> Profile:
        profile = super().save(commit=False)
        user = profile.user  # type: ignore
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

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
        help_text="Leave blank if you don't want to change the password."
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser'
        ]

    def clean_password1(self) -> Optional[str]:
        password = self.cleaned_data.get('password1')
        if password:
            # Validate password against Django's password validation rules
            try:
                validate_password(password, self.instance)
            except ValidationError as error:
                # Pass the errors to the form
                self.add_error('password1', error)
        return password

    def clean(self) -> Dict[str, Any]:
        cleaned_data = super().clean()
        if not cleaned_data:
            return {}

        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error('password2', "The two password fields didn't match.")

        return cleaned_data

    def save(self, commit: bool = True) -> Any:  # Return type as Any instead of User
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')

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
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={'accept': 'image/*'})
        }
