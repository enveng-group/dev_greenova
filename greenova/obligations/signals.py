"""Signal handlers for the obligations app.

This module contains Django signal handlers for the Obligation model.
Implements logic previously handled by django-lifecycle hooks.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging

from beartype import beartype
from django.core.exceptions import ValidationError
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Obligation

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Obligation)
@beartype
def validate_custom_aspect(sender, instance: Obligation, **kwargs) -> None:
    """Ensure custom aspect is set if needed (migrated from BEFORE_SAVE hook)."""
    if (
        instance.environmental_aspect == "Other"
        and not instance.custom_environmental_aspect
    ):
        msg = "Custom environmental aspect required if 'Other' is selected."
        raise ValidationError(msg)


@receiver(post_save, sender=Obligation)
@beartype
def update_forecasted_date_after_save(
    sender,
    instance: Obligation,
    created: bool,
    **kwargs,
) -> None:
    """Update recurring forecasted date after save if needed (migrated from AFTER_SAVE hook)."""
    if instance.recurring_obligation and not instance.recurring_forecasted_date:
        instance.update_recurring_forecasted_date()
        instance.save()


@receiver(post_save, sender=Obligation)
@beartype
def log_after_save_obligation(
    sender,
    instance: Obligation,
    created: bool,
    **kwargs,
) -> None:
    """Log after save (migrated from AFTER_SAVE hooks)."""
    logger.info("Obligation %s saved (signal)", instance.obligation_number)


@receiver(post_delete, sender=Obligation)
@beartype
def log_after_delete_obligation(sender, instance: Obligation, **kwargs) -> None:
    """Log after delete (migrated from after_delete hook)."""
    logger.info("Obligation %s deleted (signal)", instance.obligation_number)
