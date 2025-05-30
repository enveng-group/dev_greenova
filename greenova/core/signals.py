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

"""Signals for the Greenova core app.

This module defines custom and built-in Django signals for the core app,
including user login/logout and theme changes.
"""


from django.contrib.auth import get_user_model
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import Signal, receiver
from django.db.models.signals import post_save

logger = logging.getLogger(__name__)
User = get_user_model()

# Custom signals
theme_preference_changed = Signal()  # Sent when user changes theme
navigation_accessed = Signal()  # Sent when user navigates to a new section


@receiver(user_logged_in)
def log_user_login(_sender: Any, _request: Any, user: Any, **_kwargs: Any) -> None:
    """Log when a user logs in."""
    logger.info("User logged in: %s", user.username)


@receiver(user_logged_out)
def log_user_logout(_sender: Any, _request: Any, user: Any, **_kwargs: Any) -> None:
    """Log when a user logs out."""
    if user:
        logger.info("User logged out: %s", user.username)
    else:
        logger.info("Anonymous user logged out")


@receiver(post_save, sender=User)
def handle_user_update(
        _sender: Any,
        instance: Any,
        created: Any,
        **_kwargs: Any) -> None:
    """Handle user creation and updates."""
    if created:
        logger.info("New user created: %s", instance.username)
    else:
        logger.debug("User updated: %s", instance.username)
