# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the auditing app."""

from beartype import beartype
from django.core.exceptions import ValidationError

from .commons import BaseProtoSerializer
from .models import AuditEvent

try:
    from .proto_utils import (
        deserialize_audit_event,
        deserialize_audit_events,
        serialize_audit_event,
        serialize_audit_events,
    )
except ImportError:

    def serialize_audit_event(obj) -> bytes:
        return b""

    def deserialize_audit_event(data) -> None:
        return None

    def serialize_audit_events(objs) -> bytes:
        return b""

    def deserialize_audit_events(data):
        return []


class AuditEventProtoSerializer(BaseProtoSerializer):
    """Serializer for AuditEvent using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: AuditEvent | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: AuditEvent | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        audit_event = deserialize_audit_event(self.initial_data)
        if audit_event is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = audit_event
        return True

    @beartype
    def save(self) -> AuditEvent:
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    @beartype
    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        return serialize_audit_event(self.instance)


class AuditEventCollectionProtoSerializer(BaseProtoSerializer):
    """Serializer for a collection of AuditEvent instances using protobuf3."""

    @beartype
    def __init__(
        self,
        instances: list[AuditEvent] | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instances = instances
        self.initial_data = data
        self.validated_data: list[AuditEvent] | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        audit_events = deserialize_audit_events(self.initial_data)
        if not audit_events:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = audit_events
        return True

    @beartype
    def data(self) -> bytes | None:
        if self.instances is None:
            return None
        return serialize_audit_events(self.instances)
