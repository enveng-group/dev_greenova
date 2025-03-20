from typing import Dict, Any, Optional, Union
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ChatState:
    """Chat dialog state singleton."""
    _instance = None
    _state: Dict[str, Any] = {
        "isOpen": False,
        "messages": [],
        "lastUpdate": None
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_state(self) -> Dict[str, Any]:
        """Get current dialog state."""
        self._state["lastUpdate"] = datetime.now().isoformat()
        return self._state

    def toggle(self) -> Dict[str, Any]:
        """Toggle dialog open state."""
        self._state["isOpen"] = not self._state["isOpen"]
        return self.get_state()


class ChatService:
    """Handle chat-related business logic."""

    def __init__(self):
        self.state = ChatState()

    def get_dialog_state(self) -> Dict[str, Any]:
        """Get current dialog state."""
        return self.state.get_state()

    def toggle_dialog(self) -> Dict[str, Any]:
        """Toggle dialog open/closed."""
        return self.state.toggle()

    @staticmethod
    def format_message(message: str, user: str) -> Dict[str, Any]:
        """Format a chat message for display."""
        return {
            "type": "user" if user != "assistant" else "assistant",
            "content": message,
            "timestamp": "now",  # TODO: Add proper timestamp
            "sender": user
        }

    @staticmethod
    def process_message(
            message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Process an incoming chat message."""
        try:
            # TODO: Add actual message processing logic
            #
            # The variable "message" is the string input that the client has given us
            # The variable "context" is JSON data.
            #

            # This is the message that we sent the server, place this before response message...
            request_msg = f" <div class=\"chat-dialog user-dialog\">{message}</div>"

            response_text = "This is the text that we want to respond with."
            response_msg = f"<div class=\"chat-dialog chatbot-dialog\">{response_text}</div>"
            content_msg = request_msg + response_msg

            response: Dict[str, Union[str, Dict[str, Any]]] = {
                "status": "success",
                "message": content_msg,
                "context": context or {}
            }
            logger.info(f"Processed chat message: {message[:50]}...")
            return response
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "context": context or {}
            }
