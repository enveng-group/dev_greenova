from _typeshed import Incomplete
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import CustomUser as CustomUser
from .models import EnvironmentalObligation as EnvironmentalObligation
from .models import UserProfile as UserProfile

class EnvironmentalObligationForm(forms.ModelForm):
    class Meta:
        model = EnvironmentalObligation
        fields: Incomplete
        widgets: Incomplete

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields: Incomplete

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields: Incomplete

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields: Incomplete
        widgets: Incomplete

class AuditLogFilterForm(forms.Form):
    user: Incomplete
    action: Incomplete
    object_type: Incomplete
    date_from: Incomplete
    date_to: Incomplete
