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

"""Views for the chatbot app.

This module contains view functions for chatbot interactions, including
conversation management, message processing, and rendering chatbot UI.
"""


from django.views.decorators.http import require_POST
from django.http import HttpRequest
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)


@login_required
def chatbot_home(request: HttpRequest) -> None:
    """Main chatbot interface showing conversation list and a selected conversation."""
    # ...existing code...


@login_required
def create_conversation(request: HttpRequest) -> None:
    """Create a new conversation."""
    # ...existing code...


@login_required
def conversation_detail(request: HttpRequest) -> None:
    """View a specific conversation."""
    # ...existing code...


@login_required
@require_POST
def send_message(request: HttpRequest) -> None:
    """Process a new message in a conversation."""
    # ...existing code...


@login_required
def delete_conversation(request: HttpRequest) -> None:
    """Delete a conversation."""
    # ...existing code...
