"""Signal handlers for the company app.

This module contains Django signal handlers for Company and CompanyMembership models.
Implements logic previously handled by django-lifecycle hooks.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging

from beartype import beartype
from django.db.models.signals import pre_save
from django.dispatch import receiver
from slugify import slugify

from .models import Company, CompanyMembership

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Company)
@beartype
def set_company_slug(sender, instance: Company, **kwargs) -> None:
    """Set slug from name if not already set (migrated from BEFORE_SAVE hook)."""
    if not instance.slug:
        instance.slug = slugify(instance.name)


@receiver(pre_save, sender=CompanyMembership)
@beartype
def ensure_single_primary(sender, instance: CompanyMembership, **kwargs) -> None:
    """Ensure only one primary company membership per user (migrated from BEFORE_SAVE hook)."""
    if instance.is_primary:
        CompanyMembership.objects.filter(
            user=instance.user,
            is_primary=True,
        ).exclude(id=instance.id or 0).update(is_primary=False)
