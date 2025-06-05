"""
Custom type definitions and type aliases for the chatbot app.

Centralizes reusable type hints and aliases for chatbot messages, sessions,
and protocol buffers, and provides Protocols for message handlers, session
managers, and bot logic to enable strict type-safety across modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for message handlers, session managers, and bot logic

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any, Callable, Dict, List, Protocol, TypedDict, runtime_checkable
from beartype import beartype

class ChatMessageDict(TypedDict):
    """TypedDict for a chat message."""
    id: str
    sender: str
    content: str
    timestamp: str
    is_bot: bool

class SessionStateDict(TypedDict):
    """TypedDict for a chat session state."""
    session_id: str
    user_id: str
    started_at: str
    last_active: str
    context: Dict[str, Any]
    messages: List["ChatMessageDict"]

ProtoPayload = bytes

@runtime_checkable
class MessageHandler(Protocol):
    """Protocol for handling chat messages."""

    @beartype
    def __call__(self, message: ChatMessageDict) -> None:
        """Handle a chat message.

        Args:
            message: The chat message dictionary.
        """
        ...

@runtime_checkable
class SessionManager(Protocol):
    """Protocol for managing chat sessions."""

    @beartype
    def start_session(self, user_id: str) -> SessionStateDict:
        """Start a new chat session for a user.

        Args:
            user_id: The unique identifier for the user.

        Returns:
            SessionStateDict: The session state dictionary.
        """
        ...

    @beartype
    def end_session(self, session_id: str) -> None:
        """End a chat session.

        Args:
            session_id: The unique identifier for the session.
        """
        ...

    @beartype
    def get_session(self, session_id: str) -> SessionStateDict | None:
        """Retrieve a chat session by session ID.

        Args:
            session_id: The unique identifier for the session.

        Returns:
            SessionStateDict | None: The session state dictionary or None.
        """
        ...

@runtime_checkable
class BotLogic(Protocol):
    """Protocol for chatbot logic."""

    @beartype
    def process_message(
        self,
        message: ChatMessageDict,
        session: SessionStateDict,
    ) -> ChatMessageDict:
        """Process a chat message and return a response.

        Args:
            message: The incoming chat message dictionary.
            session: The current session state dictionary.

        Returns:
            ChatMessageDict: The response chat message dictionary.
        """
        ...
