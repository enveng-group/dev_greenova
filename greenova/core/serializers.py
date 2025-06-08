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
    from core.charts import (
        deserialize_mechanism,  # type: ignore[import]
        deserialize_mechanisms,  # type: ignore[import]
        serialize_mechanism,  # type: ignore[import]
        serialize_mechanisms,  # type: ignore[import],
    )
except ImportError:

    def serialize_mechanism(obj: object) -> bytes:
        return b""

    def deserialize_mechanism(data: bytes) -> None:
        return None

    def serialize_mechanisms(objs: Sequence[object]) -> bytes:
        return b""

    def deserialize_mechanisms(data: bytes) -> Sequence[object]:
        return []


try:
    from protobuf.greenova_data_pb2 import Obligation as ObligationProto
    from protobuf.greenova_data_pb2 import ObligationCollection

    PROTOBUF_AVAILABLE = True
except ImportError:
    PROTOBUF_AVAILABLE = False
    ObligationProto = None
    ObligationCollection = None

try:
    from protobuf import auditing_pb2

    AuditEntryProto = getattr(auditing_pb2, "AuditEntryProto", None)
    AuditEntryCollection = getattr(auditing_pb2, "AuditEntryCollection", None)
    AUDIT_PROTOBUF_AVAILABLE = True
except ImportError:
    AUDIT_PROTOBUF_AVAILABLE = False
    AuditEntryProto = None
    AuditEntryCollection = None

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
                "MechanismCollectionProtoSerializer: Invalid protobuf data or empty collection.", )
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
    """Convert an EnvironmentalObligation instance to a dict for serialization."""
    return {
        "id": obligation.id,
        "name": obligation.name,
        "description": obligation.description,
        "due_date": obligation.due_date.isoformat() if obligation.due_date else None,
        "is_complete": obligation.is_complete,
        "created_at": obligation.created_at.isoformat()
        if obligation.created_at
        else None,
        "updated_at": obligation.updated_at.isoformat()
        if obligation.updated_at
        else None,
    }


@beartype
def obligation_to_proto(obligation: EnvironmentalObligation) -> Any:
    """Convert an EnvironmentalObligation instance to a Protobuf Obligation message."""
    if ObligationProto is None:
        msg = "Protobuf Obligation message not available."
        raise ImportError(msg)
    proto = ObligationProto()
    proto.id = obligation.id or 0
    proto.name = obligation.name or ""
    proto.description = obligation.description or ""
    proto.due_date = obligation.due_date.isoformat() if obligation.due_date else ""
    proto.is_complete = obligation.is_complete
    proto.created_at = (
        obligation.created_at.isoformat() if obligation.created_at else ""
    )
    proto.updated_at = (
        obligation.updated_at.isoformat() if obligation.updated_at else ""
    )
    return proto


@beartype
def obligations_to_protobuf(queryset) -> bytes:
    """Serialize a queryset of EnvironmentalObligation to Protobuf bytes."""
    if ObligationProto is None:
        msg = "Protobuf Obligation message not available."
        raise ImportError(msg)
    # Assume a repeated field for obligations (define a wrapper message if needed)
    # For now, just serialize the first obligation for demo
    if queryset.count() == 1:
        return obligation_to_proto(queryset.first()).SerializeToString()
    # If multiple, return a list of serialized messages (not optimal, but demo)
    return b"".join([obligation_to_proto(obj).SerializeToString() for obj in queryset])


@beartype
def audit_log_to_proto(audit_log: Any) -> Any:
    """Convert an AuditLog instance to a Protobuf AuditEntryProto message."""
    if AuditEntryProto is None:
        msg = "Protobuf AuditEntryProto message not available."
        raise ImportError(msg)
    proto = AuditEntryProto()
    proto.id = str(audit_log.id) if audit_log.id is not None else ""
    proto.audit_id = ""  # Not available in core.AuditLog, left blank
    proto.obligation_id = audit_log.object_id or ""
    proto.status = audit_log.action or ""
    proto.finding = audit_log.message or ""
    return proto


@beartype
def audit_logs_to_protobuf(queryset) -> bytes:
    """Serialize a queryset of AuditLog to Protobuf bytes (AuditEntryCollection)."""
    if AuditEntryCollection is None:
        msg = "Protobuf AuditEntryCollection message not available."
        raise ImportError(msg)
    collection = AuditEntryCollection()
    for log in queryset:
        proto = audit_log_to_proto(log)
        collection.audit_entries.append(proto)
    return collection.SerializeToString()


@beartype
class ObligationProtoSerializer:
    """Serializer for EnvironmentalObligation objects (Protobuf3 or dict fallback)."""

    def __init__(self, obligations: Any, many: bool = False) -> None:
        self.many = many
        if many:
            self.data = [obligation_to_dict(obj) for obj in obligations]
        else:
            self.data = obligation_to_dict(obligations)

    @staticmethod
    @beartype
    def obligation_to_dict(obligation: EnvironmentalObligation) -> dict[str, Any]:
        return {
            "id": obligation.id,
            "name": obligation.name,
            "description": obligation.description,
            "due_date": obligation.due_date.isoformat()
            if obligation.due_date
            else None,
            "is_complete": obligation.is_complete,
            "created_at": obligation.created_at.isoformat()
            if obligation.created_at
            else None,
            "updated_at": obligation.updated_at.isoformat()
            if obligation.updated_at
            else None,
        }
