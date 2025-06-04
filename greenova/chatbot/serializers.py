# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the chatbot app."""

from django.core.exceptions import ValidationError

from .models import ChatbotMessage

try:
    from .proto_utils import (
        deserialize_chatbot_message,
        deserialize_chatbot_messages,
        serialize_chatbot_message,
        serialize_chatbot_messages,
    )
except ImportError:

    def serialize_chatbot_message(obj) -> bytes:
        return b""

    def deserialize_chatbot_message(data) -> None:
        return None

    def serialize_chatbot_messages(objs) -> bytes:
        return b""

    def deserialize_chatbot_messages(data):
        return []


class ChatbotMessageProtoSerializer:
    """Serializer for ChatbotMessage using protobuf3 binary format."""

    def __init__(
        self,
        instance: ChatbotMessage | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: ChatbotMessage | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
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

    def save(self) -> ChatbotMessage:
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        return serialize_chatbot_message(self.instance)


class ChatbotMessageCollectionProtoSerializer:
    """Serializer for a collection of ChatbotMessage instances using protobuf3."""

    def __init__(
        self,
        instances: list[ChatbotMessage] | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instances = instances
        self.initial_data = data
        self.validated_data: list[ChatbotMessage] | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
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

    def data(self) -> bytes | None:
        if self.instances is None:
            return None
        return serialize_chatbot_messages(self.instances)
