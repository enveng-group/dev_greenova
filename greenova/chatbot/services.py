from typing import Dict, Any, Optional, Union
import logging
from datetime import datetime

####################################
from .data.chatdata_pb2 import ChatBotResponse
from .data.chatdata_pb2 import ChatBotPrompts

# Read existing data...
prompt_list = ChatBotPrompts()
prompt_list_fname = "./chatbot/data/chatdata-serialised.protobin"

with open(prompt_list_fname, "rb") as f:
    prompt_list.ParseFromString(f.read())

####################################

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

            #
            # message ChatBotResponse {
            #     required string prompt = 1;
            #     required string response = 2;
            #     required int32 id = 3;
            # }
            #
            # message ChatBotPrompts {
            #     repeated ChatBotResponse responses = 1;
            # }
            #

            # This is the message that we sent the server, place this before response message...
            request_msg = f" <div class=\"chat-dialog user-dialog\">{message}</div>"

            response_text = "This is the text that we want to respond with."

            for response in prompt_list.responses:
                if response.prompt == message:
                    response_text = response.response

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
