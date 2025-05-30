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

"""Signals for user and profile management in the Greenova users app.

Defines signal handlers to create or update user profiles when User instances
are saved.
"""

from django.contrib.auth.models import User
from beartype import beartype
from django.db.models.signals import post_save
from .models import Profile
from django.dispatch import receiver


@receiver(post_save, sender=User)
@beartype
def create_or_update_profile(
    sender: type[User],
    instance: User,
    created: bool,
    **kwargs: dict[str, object],
) -> None:
    """Create or update the user's profile when a user is saved.

    Args:
        sender: The model class (User) that sent the signal.
        instance: The actual instance being saved.
        created: Boolean; True if a new record was created.
        **kwargs: Additional keyword arguments.

    Returns:
        None

    """
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
