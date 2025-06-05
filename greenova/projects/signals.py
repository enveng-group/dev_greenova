"""Django signal handlers for the projects app.

The post_save and post_delete logic for ProjectMembership has been migrated to django-lifecycle hooks in the model.
The m2m_changed handler for Project.members remains, as it cannot be replaced by django-lifecycle.
"""

import logging
from typing import Any
from beartype import beartype
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Project

logger = logging.getLogger(__name__)

@receiver(m2m_changed, sender=Project.members.through)
@beartype
def project_members_changed(sender: type, instance: Project, action: str, reverse: bool, model: type, pk_set: set, **kwargs: Any) -> None:
    """Handle changes to project membership.

    Args:
        sender: The model class sending the signal.
        instance: The Project instance whose members changed.
        action: The action performed (e.g., 'post_add', 'post_remove').
        reverse: Whether the relation is reversed.
        model: The model class for the related object.
        pk_set: The set of primary keys affected.
        **kwargs: Additional keyword arguments.
    """
    if action in {"post_add", "post_remove"}:
        logger.info("Project %s membership changed: %s", instance.name, action)
        # Add additional event-driven logic here (e.g., notifications)
