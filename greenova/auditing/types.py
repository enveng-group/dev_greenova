"""Custom type definitions and type aliases for the auditing app.

This module centralizes reusable type hints and aliases to improve code clarity
and maintainability across the app, and provides Protocols for serializers,
permission checkers, and protobuf utilities to enable strict type-safety
across modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for serializers, permission checkers, and protobuf utilities

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from enum import StrEnum
from typing import Any, Protocol, TypedDict, runtime_checkable

from beartype import beartype
from django.contrib.auth.models import AbstractUser


# --- Status and Data Types ---
class AuditStatus(StrEnum):
    """Enumeration of possible audit statuses."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class AuditRecordDict(TypedDict):
    """TypedDict for an audit record."""

    id: str
    obligation_id: str
    auditor: str
    status: AuditStatus
    created_at: str
    updated_at: str
    findings: list[str]
    comments: list[str]


class AuditEntryDict(TypedDict):
    """TypedDict for an audit entry."""

    id: str
    audit_id: str
    entry_type: str
    description: str
    created_at: str


AuditRecordList = list[AuditRecordDict]
AuditEntryList = list[AuditEntryDict]


# --- Protocols for Serializers, Permissions, and Protobuf Utilities ---
@runtime_checkable
class AuditEventSerializerProto(Protocol):
    """Protocol for audit event serializers (protobuf3)."""

    @beartype
    def __init__(self, instance: Any = None, data: bytes | None = None) -> None:
        """Initialize the serializer.

        Args:
            instance: The audit event instance.
            data: The protobuf binary data.

        """
        ...

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """Validate the serializer data.

        Args:
            raise_exception: Raise exception if invalid.

        Returns:
            bool: True if valid, False otherwise.

        """
        ...

    @property
    @beartype
    def validated_data(self) -> Any:
        """Get the validated data.

        Returns:
            Any: The validated data.

        """
        ...

    @beartype
    def save(self) -> Any:
        """Save the audit event.

        Returns:
            Any: The saved audit event.

        """
        ...

    @beartype
    def data(self) -> bytes | None:
        """Get the serialized protobuf data.

        Returns:
            bytes | None: The serialized data or None.

        """
        ...


@runtime_checkable
class AuditEventCollectionSerializerProto(Protocol):
    """Protocol for audit event collection serializers (protobuf3)."""

    @beartype
    def __init__(
        self,
        instances: list[Any] | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the collection serializer.

        Args:
            instances: List of audit event instances.
            data: The protobuf binary data.

        """
        ...

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """Validate the serializer data.

        Args:
            raise_exception: Raise exception if invalid.

        Returns:
            bool: True if valid, False otherwise.

        """
        ...

    @property
    @beartype
    def validated_data(self) -> list[Any]:
        """Get the validated data.

        Returns:
            List[Any]: The validated data.

        """
        ...

    @beartype
    def save(self) -> list[Any]:
        """Save the audit events.

        Returns:
            List[Any]: The saved audit events.

        """
        ...

    @beartype
    def data(self) -> bytes | None:
        """Get the serialized protobuf data.

        Returns:
            bytes | None: The serialized data or None.

        """
        ...


@runtime_checkable
class AuditPermissionChecker(Protocol):
    """Protocol for checking audit permissions."""

    @beartype
    def __call__(self, user: AbstractUser, auditlog: Any) -> bool:
        """Check if the user has permission for the audit log.

        Args:
            user: The user to check.
            auditlog: The audit log object.

        Returns:
            bool: True if permitted, False otherwise.

        """
        ...


@runtime_checkable
class AuditProtoUtils(Protocol):
    """Protocol for audit protobuf utilities."""

    @beartype
    def serialize_audit_event(self, audit_event: Any) -> bytes | None:
        """Serialize an audit event to protobuf.

        Args:
            audit_event: The audit event instance.

        Returns:
            bytes | None: The serialized data or None.

        """
        ...

    @beartype
    def deserialize_audit_event(self, data: bytes) -> Any | None:
        """Deserialize protobuf data to an audit event.

        Args:
            data: The protobuf binary data.

        Returns:
            Any | None: The deserialized audit event or None.

        """
        ...

    @beartype
    def serialize_audit_events(self, audit_events: list[Any]) -> bytes | None:
        """Serialize a list of audit events to protobuf.

        Args:
            audit_events: List of audit event instances.

        Returns:
            bytes | None: The serialized data or None.

        """
        ...

    @beartype
    def deserialize_audit_events(self, data: bytes) -> list[Any]:
        """Deserialize protobuf data to a list of audit events.

        Args:
            data: The protobuf binary data.

        Returns:
            List[Any]: The deserialized audit events.

        """
        ...


# --- Handler Protocols ---
@runtime_checkable
class AuditHandler(Protocol):
    """Protocol for audit record handlers."""

    @beartype
    def __call__(self, record: AuditRecordDict) -> None:
        """Handle an audit record.

        Args:
            record: The audit record dictionary.

        """
        ...
