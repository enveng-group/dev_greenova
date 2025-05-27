"""
Views for the chatbot app.

This module contains view functions for chatbot interactions, including
conversation management, message processing, and rendering chatbot UI.
"""
import logging

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

logger = logging.getLogger(__name__)


@login_required
def chatbot_home(request):
    """Main chatbot interface showing conversation list and a selected conversation."""
    # ...existing code...

@login_required
def create_conversation(request):
    """Create a new conversation."""
    # ...existing code...

@login_required
def conversation_detail(request, conversation_id):
    """View a specific conversation."""
    # ...existing code...

@login_required
@require_POST
def send_message(request, conversation_id):
    """Process a new message in a conversation."""
    # ...existing code...

@login_required
def delete_conversation(request, conversation_id):
    """Delete a conversation."""
    # ...existing code...
