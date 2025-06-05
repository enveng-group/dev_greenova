"""Signal handlers for the users app.

This module contains Django signal handlers for the Profile model.
Implements logic previously handled by django-lifecycle hooks.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
import os

from beartype import beartype
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

from .models import Profile

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
@beartype
def process_profile_image(sender, instance: Profile, **kwargs) -> None:
    """Resize and create thumbnail for profile image after save (migrated from lifecycle hook)."""
    if instance.profile_image:
        try:
            img_path = instance.profile_image.path
            img = Image.open(img_path)
            max_size = (400, 400)
            if img.height > 400 or img.width > 400:
                img.thumbnail(max_size)
                img.save(img_path)
            thumb_path = os.path.join(
                os.path.dirname(img_path),
                f"thumb_{os.path.basename(img_path)}",
            )
            img.thumbnail((100, 100))
            img.save(thumb_path)
        except Exception as e:
            logger.warning("Profile image processing failed: %s", e)
