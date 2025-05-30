"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Models for user and profile management in the Greenova users app.

Defines the Profile model, which extends the default Django User model with new fields.
"""

# Third-party imports
from beartype import beartype
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    """User profile model extending the default Django User model."""

    user: models.OneToOneField[User] = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile",
    )
    bio: models.TextField[str] = models.TextField(max_length=500, blank=True)
    position: models.CharField[str] = models.CharField(max_length=100, blank=True)
    department: models.CharField[str] = models.CharField(max_length=100, blank=True)
    phone_number: models.CharField[str] = models.CharField(max_length=20, blank=True)
    profile_image: models.ImageField = models.ImageField(
        upload_to="profile_images/", blank=True, null=True,
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
