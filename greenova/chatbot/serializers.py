# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the chatbot app.

This module provides serializers for converting between Django ChatbotMessage
models and Protocol Buffer messages using protobuf3 binary format.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serializers for single ChatbotMessage and collections of ChatbotMessages

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Optional

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import ChatbotMessage
from .types import ChatMessageDict, SessionStateDict

try:
    from .proto_utils import (
        deserialize_chatbot_message,
        deserialize_chatbot_messages,
        serialize_chatbot_message,
        serialize_chatbot_messages,
    )
except ImportError:

    def serialize_chatbot_message(obj: object) -> bytes:
        """Stub serialize_chatbot_message for missing proto_utils."""
        return b""

    def deserialize_chatbot_message(data: bytes) -> None:
        """Stub deserialize_chatbot_message for missing proto_utils."""
        return None

    def serialize_chatbot_messages(objs: list[object]) -> bytes:
        """Stub serialize_chatbot_messages for missing proto_utils."""
        return b""

    def deserialize_chatbot_messages(data: bytes) -> list[object]:
        """Stub deserialize_chatbot_messages for missing proto_utils."""
        return []


class ChatbotMessageProtoSerializer:
    """Serializer for ChatbotMessage using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: Optional[ChatbotMessage] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the ChatbotMessageProtoSerializer.

        Args:
            instance: Optional ChatbotMessage instance to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instance: Optional[ChatbotMessage] = instance
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[ChatbotMessage] = None
        self.errors: Optional[str] = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """
        Validate the initial protobuf data and populate validated_data.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.
        """
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        message = deserialize_chatbot_message(self.initial_data)
        if message is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = message
        return True

    @beartype
    def save(self) -> ChatbotMessage:
        """
        Save the validated ChatbotMessage instance to the database.

        Returns:
            The saved ChatbotMessage instance.

        Raises:
            ValidationError: If called before is_valid().
        """
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    @beartype
    def data(self) -> Optional[bytes]:
        """
        Serialize the ChatbotMessage instance to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instance.
        """
        if self.instance is None:
            return None
        return serialize_chatbot_message(self.instance)


class ChatbotMessageCollectionProtoSerializer:
    """Serializer for a collection of ChatbotMessage instances using protobuf3."""

    @beartype
    def __init__(
        self,
        instances: Optional[list[ChatbotMessage]] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the ChatbotMessageCollectionProtoSerializer.

        Args:
            instances: Optional list of ChatbotMessage instances to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instances: Optional[list[ChatbotMessage]] = instances
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[list[ChatbotMessage]] = None
        self.errors: Optional[str] = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """
        Validate the initial protobuf data and populate validated_data.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.
        """
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        messages = deserialize_chatbot_messages(self.initial_data)
        if not messages:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = messages
        return True

    @beartype
    def data(self) -> Optional[bytes]:
        """
        Serialize the collection of ChatbotMessage instances to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instances.
        """
        if self.instances is None:
            return None
        return serialize_chatbot_messages(self.instances)
