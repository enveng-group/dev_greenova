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

"""Signal handlers for dashboard events.

Custom dashboard events (project selection, dashboard data updates) are handled by Django signals.
Model-level event logic should be handled via django-lifecycle hooks in the relevant models.
This file is retained for custom event signals and handlers only.
"""

from django.contrib.auth.signals import user_logged_in
import logging
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
from django.http import HttpRequest
from projects.models import Project
from obligations.models import Obligation

logger = logging.getLogger(__name__)

# Custom signals
project_selected = Signal()  # Sent when a project is selected
dashboard_data_updated = Signal()  # Sent when dashboard data is updated


@receiver(project_selected)
def handle_project_selection(
    sender: object, request: HttpRequest, project_id: str | None, **kwargs: dict,
) -> None:
    """Handle project selection events.

    This signal handler ensures proper session state when a project is selected.

    Args:
        sender: The object sending the signal
        request: The current HTTP request
        project_id: The ID of the selected project
        **kwargs: Additional keyword arguments

    """
    if project_id:
        request.session["selected_project_id"] = project_id
        logger.debug("Project %s selected and stored in session", project_id)
    # Clear selection if empty project_id provided
    elif "selected_project_id" in request.session:
        del request.session["selected_project_id"]
        logger.debug("Project selection cleared from session")

    # Ensure session changes are saved
    request.session.modified = True


@receiver(user_logged_in)
def restore_dashboard_state(
    sender: object, request: HttpRequest, user: object, **kwargs: dict,
) -> None:
    """Restore dashboard state when a user logs in.

    This ensures continuity of experience across login sessions.

    Args:
        sender: The object sending the signal
        request: The current HTTP request
        user: The user who just logged in
        **kwargs: Additional keyword arguments

    """
    # Nothing to do if there's no request
    if not request:
        return

    # Check if user had a previously selected project
    try:
        # Try to get the user's last accessed project
        last_project = (
            Project.objects.filter(members=user).order_by("-last_accessed").first()
        )

        if last_project:
            request.session["selected_project_id"] = str(last_project.id)
            logger.debug(
                "Restored last accessed project %s for user %s",
                last_project.id,
                user.username,
            )
    except Exception as e:
        logger.exception("Error restoring dashboard state: %s", str(e))


@receiver(post_save, sender=Obligation)
def update_dashboard_data(
    sender: object, instance: Obligation, **kwargs: dict,
) -> None:
    """Signal handler to update dashboard data when obligations change.

    Args:
        sender: The model class sending the signal
        instance: The Obligation instance that was saved
        **kwargs: Additional keyword arguments

    """
    # This currently just logs the event
    # In a real-time application, this might trigger WebSocket updates
    logger.debug("Dashboard data updated due to change in obligation %s", instance.id)

    # Send the custom signal
    dashboard_data_updated.send(
        sender=sender,
        obligation_id=instance.id,
        project_id=instance.project_id if hasattr(instance, "project") else None,
    )
