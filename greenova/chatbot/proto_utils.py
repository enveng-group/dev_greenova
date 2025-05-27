# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Protocol buffer utilities for the chatbot app.

This module provides serialization and deserialization functions for
converting between Django models and Protocol Buffer messages in the
chatbot application.
"""

import logging
import os

from django.contrib.auth import get_user_model

# Import datetime explicitly to fix the module attribute error

User = get_user_model()
logger = logging.getLogger(__name__)


# Create minimal stubs for the protocol buffer classes
class DummyMessage:
    """Stub class used when protocol buffers are not available."""

    def serializetostring(self) -> bytes:
        """Serialize the message to bytes (stub)."""
        return b""

    def parsefromstring(self, data: bytes) -> None:
        """Parse the message from bytes (stub)."""


# Import generated protobuf modules with improved error handling
try:
    # Use relative import to ensure consistent module path
    from .proto import chatbot_pb2

    logger.info("Successfully imported chatbot_pb2 from proto package")
except ImportError:
    logger.error("Failed to import chatbot_pb2. Protocol buffer definition missing.")

    # Check if the proto file exists
    current_dir = os.path.dirname(os.path.abspath(__file__))
    proto_file = os.path.join(current_dir, "proto", "chatbot.proto")

    if os.path.exists(proto_file):
        logger.info(
            "chatbot.proto exists but chatbot_pb2.py not found. "
            "Run 'python manage.py compile_protos --app=chatbot' to generate it."
        )
    else:
        logger.error("chatbot.proto file not found in the proto directory.")

    # Create a minimal stub for the module to allow Django to continue loading
    chatbot_pb2 = type("chatbot_pb2", (), {})

    # Define minimal classes needed for type hinting
    class ChatMessage(DummyMessage):
        """Minimal ChatMessage stub for type hinting."""
        class MessageType:
            """Enum for message types."""
            MESSAGE_TYPE_TEXT_UNSPECIFIED = 0
            MESSAGE_TYPE_IMAGE = 1
            MESSAGE_TYPE_AUDIO = 2

        def __init__(self):
            """Initialize a ChatMessage stub."""
            self.user_id = ""
            self.content = ""
            self.timestamp = 0
            self.type = self.MessageType.MESSAGE_TYPE_TEXT_UNSPECIFIED

    class ChatResponse(DummyMessage):
        """Minimal ChatResponse stub for type hinting."""

        def __init__(self):
            """Initialize a ChatResponse stub."""
            self.message_id = ""
            self.content = ""
            self.timestamp = 0

    chatbot_pb2.ChatMessage = ChatMessage
    chatbot_pb2.ChatResponse = ChatResponse

# ...existing code...
