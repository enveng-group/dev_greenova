# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Protocol buffer utilities for the chatbot app.

This module provides serialization and deserialization functions for
converting between Django models and Protocol Buffer messages in the
chatbot application.
"""
import datetime
import logging
import os
import sys
import time
from typing import Optional

from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()
logger = logging.getLogger(__name__)

# Import generated protobuf modules with improved error handling
try:
    from .proto import chatbot_pb2
except ImportError:
    logger.error("Failed to import chatbot_pb2. Protocol buffer definition missing.")

    # Check if the proto file exists
    current_dir = os.path.dirname(os.path.abspath(__file__))
    proto_file = os.path.join(current_dir, 'proto', 'chatbot.proto')

    if os.path.exists(proto_file):
        logger.info(
            "chatbot.proto exists but chatbot_pb2.py not found. "
            "Run 'python manage.py compile_protos --app=chatbot' to generate it."
        )
    else:
        logger.error("chatbot.proto file not found in the proto directory.")

    # Create a minimal stub for the module to allow Django to continue loading
    from types import ModuleType
    chatbot_pb2 = ModuleType('chatbot_pb2')
    sys.modules['chatbot.proto.chatbot_pb2'] = chatbot_pb2

    # Define minimal classes needed for type hinting
    class ChatMessage:
        class MessageType:
            MESSAGE_TYPE_TEXT_UNSPECIFIED = 0
            MESSAGE_TYPE_IMAGE = 1
            MESSAGE_TYPE_AUDIO = 2

        def __init__(self):
            self.user_id = ""
            self.content = ""
            self.timestamp = 0
            self.type = self.MessageType.MESSAGE_TYPE_TEXT_UNSPECIFIED

        def SerializeToString(self):
            return b''

        def ParseFromString(self, data):
            pass

    class ChatResponse:
        def SerializeToString(self):
            return b''

        def ParseFromString(self, data):
            pass

    chatbot_pb2.ChatMessage = ChatMessage
    chatbot_pb2.ChatResponse = ChatResponse

try:
    from . import chatbot_pb2
except ImportError:
    logger.error("chatbot_pb2 module not found. Ensure to compile the protobuf files.")
    chatbot_pb2 = None

def serialize_chat_message(chat_message) -> Optional[bytes]:
    """
    Serialize a ChatMessage instance to a Protocol Buffer message.

    Args:
        chat_message: The ChatMessage instance to serialize

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed
    """
    try:
        # Create a new ChatMessage message
        proto = chatbot_pb2.ChatMessage()

        # Set basic fields
        if hasattr(chat_message, 'user') and chat_message.user:
            # Initialize attributes properly
            proto = build_chat_message_proto(
                user_id=str(chat_message.user.id),
                content=chat_message.content,
                timestamp=(
                    int(chat_message.timestamp.timestamp())
                    if hasattr(chat_message, 'timestamp') else None
                ),
                message_type=(
                    chatbot_pb2.ChatMessage.MessageType.MESSAGE_TYPE_TEXT_UNSPECIFIED
                )
            )
        else:
            # If no user, still set other attributes
            timestamp = None
            if hasattr(chat_message, 'timestamp'):
                timestamp = int(chat_message.timestamp.timestamp())

            message_type = (
                chatbot_pb2.ChatMessage.MessageType.MESSAGE_TYPE_TEXT_UNSPECIFIED
            )

            proto = build_chat_message_proto(
                user_id=None,
                content=chat_message.content,
                timestamp=timestamp,
                message_type=message_type
            )

        # Serialize to bytes
        return proto.SerializeToString()
    except ValueError as e:
        logger.error("Value error during chat message serialization: %s", str(e))
        return None
    except AttributeError as e:
        logger.error("Attribute error during chat message serialization: %s", str(e))
        return None
    except TypeError as e:
        logger.error("Type error during chat message serialization: %s", str(e))
        return None
    except (OverflowError, MemoryError, RuntimeError) as e:
        logger.error("Runtime error during chat message serialization: %s", str(e))
        return None


def build_chat_message_proto(user_id, content, timestamp, message_type):
    """
    Build a ChatMessage protobuf object with proper initialization.

    Args:
        user_id: User ID string or None
        content: Message content string
        timestamp: Message timestamp as Unix timestamp or None
        message_type: Message type enum value

    Returns:
        Initialized ChatMessage protobuf object
    """
    proto = chatbot_pb2.ChatMessage()

    if user_id is not None:
        proto.user_id = user_id

    proto.content = content

    if timestamp is not None:
        proto.timestamp = timestamp

    proto.type = message_type

    return proto


def deserialize_chat_message(data: bytes) -> Optional[dict]:
    """
    Deserialize Protocol Buffer data to a dictionary that can be used to create
    a ChatMessage.

    Args:
        data: Serialized protocol buffer data

    Returns:
        A dictionary with ChatMessage fields, or None if deserialization failed
    """
    try:
        # Parse the binary data into a ChatMessage
        proto = chatbot_pb2.ChatMessage()
        proto.ParseFromString(data)

        # Convert to a dictionary
        message_dict = {
            'content': proto.content,
        }

        # Add user if present
        if proto.user_id:
            try:
                user = User.objects.get(id=int(proto.user_id))
                message_dict['user'] = user
            except (User.DoesNotExist, ValueError):
                logger.warning("User with ID %s not found", proto.user_id)

        # Add timestamp if present
        if proto.timestamp:
            message_dict['timestamp'] = timezone.make_aware(
                datetime.datetime.fromtimestamp(proto.timestamp)
            )

        return message_dict
    except ValueError as e:
        logger.error("Value error during message deserialization: %s", str(e))
        return None
    except AttributeError as e:
        logger.error("Attribute error during message deserialization: %s", str(e))
        return None
    except TypeError as e:
        logger.error("Type error during message deserialization: %s", str(e))
        return None
    except (KeyError, IndexError, OverflowError) as e:
        logger.error("Data structure error during message deserialization: %s", str(e))
        return None


def create_chat_response(message_id: str, content: str) -> Optional[bytes]:
    """
    Create a serialized ChatResponse protocol buffer message.

    Args:
        message_id: The ID of the message being responded to
        content: The content of the response

    Returns:
        Serialized protocol buffer data as bytes, or None if creation failed
    """
    try:
        # Create a new ChatResponse message
        proto = chatbot_pb2.ChatResponse()

        # Set fields
        proto.message_id = message_id
        proto.content = content

        # Set timestamp
        proto.timestamp = int(time.time())

        # Serialize to bytes
        return proto.SerializeToString()
    except ValueError as e:
        logger.error("Value error during chat response creation: %s", str(e))
        return None
    except AttributeError as e:
        logger.error("Attribute error during chat response creation: %s", str(e))
        return None
    except TypeError as e:
        logger.error("Type error during chat response creation: %s", str(e))
        return None
    except (OverflowError, MemoryError) as e:
        logger.error("Resource error during chat response creation: %s", str(e))
        return None


def parse_chat_response(data: bytes) -> Optional[dict]:
    """
    Parse a serialized ChatResponse protocol buffer message.

    Args:
        data: Serialized protocol buffer data

    Returns:
        A dictionary with the response data, or None if parsing failed
    """
    try:
        # Parse the binary data into a ChatResponse
        proto = chatbot_pb2.ChatResponse()
        proto.ParseFromString(data)

        # Convert to a dictionary
        response_dict = {
            'message_id': proto.message_id,
            'content': proto.content,
        }

        # Add timestamp if present
        if proto.timestamp:
            response_dict['timestamp'] = timezone.make_aware(
                datetime.datetime.fromtimestamp(proto.timestamp)
            )

        return response_dict
    except ValueError as e:
        logger.error("Value error during chat response parsing: %s", str(e))
        return None
    except AttributeError as e:
        logger.error("Attribute error during chat response parsing: %s", str(e))
        return None
    except TypeError as e:
        logger.error("Type error during chat response parsing: %s", str(e))
        return None
    except (KeyError, IndexError, OverflowError) as e:
        logger.error("Data structure error during chat response parsing: %s", str(e))
        return None
