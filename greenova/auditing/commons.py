"""commons.py.

Shared logic, helpers, and base classes for the auditing app.

This module centralizes reusable code to improve maintainability and reduce duplication.
"""

from typing import Any

from beartype import beartype
from .types import AuditRecordDict, AuditEntryDict

# Shared error messages for protobuf serialization/deserialization
PROTOBUF_ERROR_MESSAGES = {
    "serialize": "Failed to serialize audit event.",
    "deserialize": "Failed to deserialize audit event.",
    "serialize_collection": "Failed to serialize audit events collection.",
    "deserialize_collection": "Failed to deserialize audit events collection.",
}


class BaseProtoSerializer:
    """Base serializer for protobuf3-based serializers."""

    @beartype
    def __init__(self, instance: Any | None = None, data: bytes | None = None) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: Any | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        raise NotImplementedError

    @beartype
    def save(self) -> Any:
        raise NotImplementedError

    @beartype
    def data(self) -> bytes | None:
        raise NotImplementedError


# Add additional shared helpers or base classes here as needed.
