"""commons.py.

Shared logic, helpers, and base classes for the chatbot app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

from typing import Any

from beartype import beartype
from .types import ChatMessageDict, SessionStateDict


@beartype
def format_chat_message(sender: str, message: str, timestamp: str) -> dict[str, Any]:
    """Format a chat message for consistent display and serialization.

    Args:
        sender: The sender's name or identifier.
        message: The message content.
        timestamp: The message timestamp as a string.

    Returns:
        A dictionary representing the formatted chat message.

    """
    return {
        "sender": sender,
        "message": message.strip(),
        "timestamp": timestamp,
    }


@beartype
def is_valid_message(message: str) -> bool:
    """Check if a chat message is valid (non-empty, not just whitespace)."""
    return bool(message and message.strip())


# Add additional shared helpers or base classes here as needed.
