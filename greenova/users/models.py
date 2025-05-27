"""Models for user and profile management in the Greenova users app.

Defines the Profile model, which extends the default Django User model with new fields.
"""

from beartype import beartype
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """User profile model extending the default Django User model."""

    user: models.OneToOneField[User] = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile"
    )
    bio: models.TextField[str] = models.TextField(max_length=500, blank=True)
    position: models.CharField[str] = models.CharField(max_length=100, blank=True)
    department: models.CharField[str] = models.CharField(max_length=100, blank=True)
    phone_number: models.CharField[str] = models.CharField(max_length=20, blank=True)
    profile_image: models.ImageField = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    @beartype
    def __str__(self) -> str:
        """Return a string representation of the profile.

        Returns:
            A string with the user's username and 'profile' label.
        """
        return f"{self.user.username}'s profile"
