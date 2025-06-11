from .models import Profile
from _typeshed import Incomplete
from django import forms
from django.db.models import Model
from typing import Any, TypeVar

User: Incomplete
T = TypeVar('T', bound=Model)

class UserProfileForm(forms.ModelForm):
    first_name: Incomplete
    last_name: Incomplete
    email: Incomplete
    class Meta:
        model = Profile
        fields: Incomplete
        widgets: Incomplete
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def save(self, commit: bool = True) -> Profile: ...

class AdminUserForm(forms.ModelForm):
    password1: Incomplete
    password2: Incomplete
    class Meta:
        model = User
        fields: Incomplete
    def clean_password1(self) -> str | None: ...
    def clean(self) -> dict[str, Any]: ...
    def save(self, commit: bool = True) -> Any: ...

class ProfileImageForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields: Incomplete
        widgets: Incomplete
