"""Signal handlers for the projects app.

This module contains Django signal handlers for ProjectMembership model.
Implements logic previously handled by django-lifecycle hooks.

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging

from beartype import beartype
from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver

from .models import Project, ProjectMembership

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ProjectMembership)
@beartype
def after_save_membership(
    sender,
    instance: ProjectMembership,
    created: bool,
    **kwargs,
) -> None:
    """Handle logic after saving a project membership (migrated from lifecycle hook)."""
    logger.info(
        "ProjectMembership %s saved (signal, replaces lifecycle hook)",
        instance,
    )
    # Add additional event-driven logic here as needed


@receiver(post_delete, sender=ProjectMembership)
@beartype
def after_delete_membership(sender, instance: ProjectMembership, **kwargs) -> None:
    """Handle logic after deleting a project membership (migrated from lifecycle hook)."""
    logger.info(
        "ProjectMembership %s deleted (signal, replaces lifecycle hook)",
        instance,
    )
    # Add additional cleanup or notification logic here as needed


@receiver(m2m_changed, sender=Project.members.through)
@beartype
def project_members_changed(
    sender,
    instance: Project,
    action: str,
    reverse: bool,
    model: type,
    pk_set: set,
    **kwargs,
) -> None:
    """Handle changes to project membership (existing logic)."""
    if action in {"post_add", "post_remove"}:
        logger.info("Project %s membership changed: %s", instance.name, action)
        # Add additional event-driven logic here (e.g., notifications)
