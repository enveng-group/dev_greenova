# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

"""Serializers for EnvironmentalMechanism and EnvironmentalObligation Protobuf integration.

Provides serialization and deserialization logic for EnvironmentalMechanism
and EnvironmentalObligation objects using Protobuf3, with strict type safety
and runtime validation.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

import logging
from collections.abc import Sequence
from typing import Any

from beartype import beartype
from core.models import EnvironmentalObligation
from django.core.exceptions import ValidationError
from mechanisms.models import EnvironmentalMechanism

try:
    from protobuf.auditing_pb2 import (
        AuditEntryCollection,  # type: ignore
        AuditEntryProto,
    )
    from protobuf.greenova_data_pb2 import Obligation as ObligationProto  # type: ignore
    from protobuf.greenova_data_pb2 import ObligationCollection  # type: ignore
except ImportError:
    ObligationProto = None  # type: ignore
    ObligationCollection = None  # type: ignore
    AuditEntryProto = None  # type: ignore
    AuditEntryCollection = None  # type: ignore

try:
    from protobuf.core_audit_pb2 import (
        AuditLogCollection,  # type: ignore
        AuditLogProto,  # type: ignore
    )
except ImportError as e:
    AuditLogProto = None  # type: ignore
    AuditLogCollection = None  # type: ignore
    logging.getLogger(__name__).exception(f"Protobuf import error: {e}")

logger = logging.getLogger(__name__)


class MechanismProtoSerializer:
    """Serializer for a single EnvironmentalMechanism using Protobuf3."""

    @beartype
    def __init__(
        self,
        instance: EnvironmentalMechanism | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the serializer.

        Args:
            instance: An EnvironmentalMechanism instance to serialize.
            data: Protobuf-encoded bytes to deserialize.

        """
        self.instance: EnvironmentalMechanism | None = instance
        self.initial_data: bytes | None = data
        self.validated_data: EnvironmentalMechanism | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """Validate and deserialize the input data.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.

        """
        if self.initial_data is None:
            self.errors = "No data provided."
            logger.warning("MechanismProtoSerializer: No data provided.")
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        mechanism = deserialize_mechanism(self.initial_data)
        if mechanism is None:
            self.errors = "Invalid protobuf data."
            logger.error("MechanismProtoSerializer: Invalid protobuf data.")
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = mechanism
        return True

    @beartype
    def save(self) -> EnvironmentalMechanism:
        """Save the validated EnvironmentalMechanism instance.

        Returns:
            The saved EnvironmentalMechanism instance.

        Raises:
            ValidationError: If called before validation.

        """
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            logger.error("MechanismProtoSerializer: %s", msg)
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        logger.info("MechanismProtoSerializer: Saved instance %s", self.instance)
        return self.instance

    @beartype
    def data(self) -> bytes | None:
        """Serialize the instance to Protobuf bytes.

        Returns:
            Protobuf-encoded bytes, or None if no instance.

        """
        if self.instance is None:
            logger.warning("MechanismProtoSerializer: No instance to serialize.")
            return None
        return serialize_mechanism(self.instance)


class MechanismCollectionProtoSerializer:
    """Serializer for a collection of EnvironmentalMechanism objects."""

    @beartype
    def __init__(
        self,
        instances: Sequence[EnvironmentalMechanism] | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the collection serializer.

        Args:
            instances: Sequence of EnvironmentalMechanism objects.
            data: Protobuf-encoded bytes to deserialize.

        """
        self.instances: Sequence[EnvironmentalMechanism] | None = instances
        self.initial_data: bytes | None = data
        self.validated_data: Sequence[EnvironmentalMechanism] | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """Validate and deserialize the input data for a collection.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.

        """
        if self.initial_data is None:
            self.errors = "No data provided."
            logger.warning("MechanismCollectionProtoSerializer: No data provided.")
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        mechanisms = deserialize_mechanisms(self.initial_data)
        if not mechanisms:
            self.errors = "Invalid protobuf data or empty collection."
            logger.error(
                "MechanismCollectionProtoSerializer: Invalid protobuf data or empty collection."
            )
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = mechanisms  # type: ignore[assignment]
        return True

    @beartype
    def data(self) -> bytes | None:
        """Serialize the collection to Protobuf bytes.

        Returns:
            Protobuf-encoded bytes, or None if no instances.

        """
        if self.instances is None:
            logger.warning(
                "MechanismCollectionProtoSerializer: No instances to serialize.",
            )
            return None
        return serialize_mechanisms(self.instances)  # type: ignore[arg-type]


@beartype
def obligation_to_dict(obligation: EnvironmentalObligation) -> dict[str, Any]:
    """Convert an EnvironmentalObligation instance to a dict for serialization.

    Args:
        obligation: The EnvironmentalObligation instance.

    Returns:
        A dictionary representation of the object.

    """
    return {
        "id": getattr(obligation, "id", None),
        "name": getattr(obligation, "name", ""),
    }


@beartype
def obligation_to_proto(obligation: EnvironmentalObligation) -> object:
    """Convert an EnvironmentalObligation instance to a Protobuf Obligation message.

    Args:
        obligation: The EnvironmentalObligation instance.

    Returns:
        A Protobuf Obligation message instance.

    Raises:
        ImportError: If Protobuf is not available.

    """
    if ObligationProto is None:
        msg = "Protobuf Obligation message not available."
        raise ImportError(msg)
    proto = ObligationProto()  # type: ignore
    proto.id = getattr(obligation, "id", 0)  # type: ignore
    proto.name = getattr(obligation, "name", "")  # type: ignore
    return proto  # type: ignore


@beartype
def obligations_to_protobuf(queryset: Sequence[EnvironmentalObligation]) -> bytes:
    """Serialize a queryset of EnvironmentalObligation to Protobuf bytes.

    Args:
        queryset: A sequence of EnvironmentalObligation instances.

    Returns:
        Protobuf-serialized bytes.

    Raises:
        ImportError: If Protobuf is not available.

    """
    if ObligationProto is None or ObligationCollection is None:
        msg = "Protobuf Obligation message not available."
        raise ImportError(msg)
    collection = ObligationCollection()  # type: ignore
    for obj in queryset:
        collection.obligations.add().CopyFrom(obligation_to_proto(obj))  # type: ignore
    return collection.SerializeToString()  # type: ignore


@beartype
def serialize_audit_log_to_proto(audit_log: object) -> object:
    """Alias for audit_log_to_proto for test compatibility."""
    return audit_log_to_proto(audit_log)


@beartype
def serialize_audit_log_collection_to_proto(queryset: Sequence[object]) -> object:
    """Return an AuditLogCollection (not bytes) for test compatibility."""
    if AuditLogCollection is None:
        msg = "Protobuf AuditLogCollection message not available."
        raise ImportError(msg)
    logs = list(queryset)
    collection = AuditLogCollection()  # type: ignore
    for log in logs:
        collection.audit_logs.add().CopyFrom(audit_log_to_proto(log))  # type: ignore
    return collection  # type: ignore


@beartype
def audit_log_to_proto(audit_log: object) -> object:
    """Convert an AuditLog instance to a Protobuf AuditLogProto message.

    Args:
        audit_log: The AuditLog instance.

    Returns:
        A Protobuf AuditLogProto message instance.

    Raises:
        ImportError: If Protobuf is not available.

    """
    if AuditLogProto is None:
        msg = "Protobuf AuditLogProto message not available."
        raise ImportError(msg)
    proto = AuditLogProto()  # type: ignore
    proto.id = str(getattr(audit_log, "id", ""))  # type: ignore
    proto.user_id = str(
        getattr(audit_log, "user_id", getattr(audit_log, "user", "") or "")
    )  # type: ignore
    proto.action = getattr(audit_log, "action", "") or ""  # type: ignore
    proto.object_type = getattr(audit_log, "object_type", "") or ""  # type: ignore
    proto.object_id = str(getattr(audit_log, "object_id", ""))  # type: ignore
    proto.message = getattr(audit_log, "message", "") or ""  # type: ignore
    proto.ip_address = getattr(audit_log, "ip_address", "") or ""  # type: ignore
    proto.timestamp = str(getattr(audit_log, "timestamp", ""))  # type: ignore
    return proto  # type: ignore


@beartype
def audit_logs_to_protobuf(queryset: Sequence[object]) -> bytes:
    """Serialize a queryset of AuditLog to Protobuf bytes (AuditLogCollection).

    Args:
        queryset: A sequence of AuditLog instances.

    Returns:
        Protobuf-serialized bytes.

    Raises:
        ImportError: If Protobuf is not available.

    """
    if AuditLogCollection is None:
        msg = "Protobuf AuditLogCollection message not available."
        raise ImportError(msg)
    logs = list(queryset)
    collection = AuditLogCollection()  # type: ignore
    for log in logs:
        collection.audit_logs.add().CopyFrom(audit_log_to_proto(log))  # type: ignore
    return collection.SerializeToString()  # type: ignore


@beartype
class ObligationProtoSerializer:
    """Serializer for EnvironmentalObligation objects (Protobuf3 or dict fallback)."""

    def __init__(self, obligations: Any, many: bool = False) -> None:
        """Initialize the serializer.

        Args:
            obligations: The EnvironmentalObligation instances.
            many: Whether to serialize multiple instances.

        """
        self.many = many
        if many:
            self.data = [obligation_to_dict(obj) for obj in obligations]
        else:
            self.data = obligation_to_dict(obligations)

    @staticmethod
    @beartype
    def obligation_to_dict(obligation: EnvironmentalObligation) -> dict[str, Any]:
        """Convert an EnvironmentalObligation instance to a dict.

        Args:
            obligation: The EnvironmentalObligation instance.

        Returns:
            A dictionary representation of the obligation.

        """
        return {
            "id": obligation.id,
            "name": obligation.name,
            "description": obligation.description,
            "due_date": (
                obligation.due_date.isoformat() if obligation.due_date else None
            ),
            "is_complete": obligation.is_complete,
            "created_at": (
                obligation.created_at.isoformat() if obligation.created_at else None
            ),
            "updated_at": (
                obligation.updated_at.isoformat() if obligation.updated_at else None
            ),
        }


class EnvironmentalObligationSerializer:
    """Serializer for EnvironmentalObligation model."""

    @beartype
    def serialize(self, obj: EnvironmentalObligation) -> dict[str, str | int]:
        """Serialize an EnvironmentalObligation instance to a dict.

        Args:
            obj: The EnvironmentalObligation instance.

        Returns:
            A dictionary representation of the object.

        """
        return {"id": getattr(obj, "id", 0), "name": getattr(obj, "name", "")}
