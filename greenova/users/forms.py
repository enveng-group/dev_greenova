from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'job_title', 'department', 'phone', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }