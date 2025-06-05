# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the chatbot app.

This module provides serialization and deserialization functions for
converting between Django models and Protocol Buffer messages in the
chatbot application.

Features:
    - Safe import and fallback stubs for protobufs
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serialization/deserialization helpers for ChatMessage and ChatResponse

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any, Dict, Optional

from beartype import beartype
from django.contrib.auth import get_user_model
from django.utils import timezone

from .types import ChatMessageDict, SessionStateDict

User = get_user_model()
logger = logging.getLogger(__name__)


class DummyMessage:
    """Stub class used when protocol buffers are not available."""

    @beartype
    def SerializeToString(self) -> bytes:
        """Serialize the dummy message to bytes.

        Returns:
            Empty bytes object.
        """
        return b""

    @beartype
    def ParseFromString(self, data: bytes) -> None:
        """Parse the dummy message from bytes.

        Args:
            data: Bytes to parse (ignored).
        """
        pass


# Import generated protobuf modules with improved error handling
try:
    try:
        from chatbot.proto import chatbot_pb2

        logger.info("Successfully imported chatbot_pb2 from top-level")
    except ImportError:
        from chatbot.proto import chatbot_pb2

        logger.info("Successfully imported chatbot_pb2 from proto package")
except ImportError:
    logger.exception(
        "Failed to import chatbot_pb2. Protocol buffer definition missing.",
    )

    current_dir = os.path.dirname(os.path.abspath(__file__))
    proto_file = os.path.join(current_dir, "proto", "chatbot.proto")

    if os.path.exists(proto_file):
        logger.info(
            "chatbot.proto exists but chatbot_pb2.py not found. "
            "Run 'python manage.py compile_protos --app=chatbot' to generate it.",
        )
    else:
        logger.exception("chatbot.proto file not found in the proto directory.")

    chatbot_pb2 = type("chatbot_pb2", (), {})

    class ChatMessage(DummyMessage):
        """Minimal ChatMessage stub for type hinting."""

        class MessageType:
            MESSAGE_TYPE_TEXT_UNSPECIFIED = 0
            MESSAGE_TYPE_IMAGE = 1
            MESSAGE_TYPE_AUDIO = 2

        @beartype
        def __init__(self) -> None:
            """Initialize stub ChatMessage fields."""
            self.user_id: str = ""
            self.content: str = ""
            self.timestamp: int = 0
            self.type: int = self.MessageType.MESSAGE_TYPE_TEXT_UNSPECIFIED

    class ChatResponse(DummyMessage):
        """Minimal ChatResponse stub for type hinting."""

        @beartype
        def __init__(self) -> None:
            """Initialize stub ChatResponse fields."""
            self.message_id: str = ""
            self.content: str = ""
            self.timestamp: int = 0

    chatbot_pb2.ChatMessage = ChatMessage
    chatbot_pb2.ChatResponse = ChatResponse


@beartype
def serialize_chat_message(chat_message: Any) -> Optional[bytes]:
    """Serialize a ChatMessage instance to a Protocol Buffer message.

    Args:
        chat_message: The ChatMessage instance to serialize.

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed.

    Raises:
        AttributeError: If required fields are missing.
        Exception: For any serialization error.
    """
    try:
        proto = chatbot_pb2.ChatMessage()
        if hasattr(chat_message, "user") and chat_message.user:
            proto.user_id = str(chat_message.user.id)
        proto.content = chat_message.content
        proto.timestamp = int(chat_message.timestamp.timestamp())
        proto.type = chatbot_pb2.ChatMessage.MessageType.MESSAGE_TYPE_TEXT_UNSPECIFIED
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Error during chat message serialization: %s", str(e))
        return None


@beartype
def build_chat_message_proto(
    user_id: Optional[str],
    content: str,
    timestamp: Optional[int],
    message_type: int,
) -> Any:
    """Build a ChatMessage protobuf object with proper initialization.

    Args:
        user_id: User ID string or None.
        content: Message content string.
        timestamp: Message timestamp as Unix timestamp or None.
        message_type: Message type enum value.

    Returns:
        Initialized ChatMessage protobuf object.
    """
    proto = chatbot_pb2.ChatMessage()
    if user_id is not None:
        proto.user_id = user_id
    proto.content = content
    if timestamp is not None:
        proto.timestamp = timestamp
    proto.type = message_type
    return proto


@beartype
def deserialize_chat_message(data: bytes) -> Optional[Dict[str, Any]]:
    """Deserialize Protocol Buffer data to a dictionary for ChatMessage creation.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        A dictionary with ChatMessage fields, or None if deserialization failed.

    Raises:
        Exception: For any deserialization error.
    """
    try:
        proto = chatbot_pb2.ChatMessage()
        proto.ParseFromString(data)
        message_dict: Dict[str, Any] = {
            "content": proto.content,
        }
        if getattr(proto, "user_id", None):
            try:
                message_dict["user"] = User.objects.get(id=proto.user_id)
            except User.DoesNotExist:
                logger.warning("User with ID %s not found", proto.user_id)
        if getattr(proto, "timestamp", None):
            message_dict["timestamp"] = timezone.datetime.fromtimestamp(
                proto.timestamp,
                tz=timezone.get_current_timezone(),
            )
        return message_dict
    except Exception as e:
        logger.exception("Error during message deserialization: %s", str(e))
        return None


@beartype
def create_chat_response(message_id: str, content: str) -> Optional[bytes]:
    """Create a serialized ChatResponse protocol buffer message.

    Args:
        message_id: The ID of the message being responded to.
        content: The content of the response.

    Returns:
        Serialized protocol buffer data as bytes, or None if creation failed.

    Raises:
        Exception: For any serialization error.
    """
    try:
        proto = chatbot_pb2.ChatResponse()
        proto.message_id = str(message_id)
        proto.content = content
        proto.timestamp = int(time.time())
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Error during chat response creation: %s", str(e))
        return None


@beartype
def parse_chat_response(data: bytes) -> Optional[Dict[str, Any]]:
    """Parse a serialized ChatResponse protocol buffer message.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        A dictionary with the response data, or None if parsing failed.

    Raises:
        Exception: For any deserialization error.
    """
    try:
        proto = chatbot_pb2.ChatResponse()
        proto.ParseFromString(data)
        response_dict: Dict[str, Any] = {
            "message_id": proto.message_id,
            "content": proto.content,
        }
        if getattr(proto, "timestamp", None):
            response_dict["timestamp"] = timezone.datetime.fromtimestamp(
                proto.timestamp,
                tz=timezone.get_current_timezone(),
            )
        return response_dict
    except Exception as e:
        logger.exception("Error during chat response parsing: %s", str(e))
        return None
