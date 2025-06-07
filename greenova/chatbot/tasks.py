"""Background and manual tasks for the chatbot app.

All functions and classes are decorated with @beartype for runtime type checking.
"""

import logging

from beartype import beartype
from django.utils import timezone

from .models import Conversation

logger = logging.getLogger(__name__)


@beartype
def process_pending_messages() -> None:
    """Process and mark as sent any unsent chat messages in all conversations."""
    now = timezone.now()
    count = 0
    for conversation in Conversation.objects.all():
        unsent = conversation.messages.filter(sent=False)
        for message in unsent:
            # Here you would implement actual delivery logic (e.g., push, email, etc.)
            message.sent = True
            message.sent_at = now
            message.save()
            count += 1
    logger.info("Processed and marked %d pending chat messages as sent", count)
