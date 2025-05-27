"""Signals for user and profile management in the Greenova users app.

Defines signal handlers to create or update user profiles when User instances
are saved.
"""

from beartype import beartype
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


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
