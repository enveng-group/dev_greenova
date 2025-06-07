# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the responsibility app."""

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import Responsibility, ResponsibilityAssignment

try:
    from .proto_utils import (
        deserialize_responsibilities,
        deserialize_responsibility,
        deserialize_responsibility_assignment,
        deserialize_responsibility_assignments,
        serialize_responsibilities,
        serialize_responsibility,
        serialize_responsibility_assignment,
        serialize_responsibility_assignments,
    )
except ImportError:

    def serialize_responsibility(obj) -> bytes:
        return b""

    def deserialize_responsibility(data) -> None:
        return None

    def serialize_responsibilities(objs) -> bytes:
        return b""

    def deserialize_responsibilities(data):
        return []

    def serialize_responsibility_assignment(obj) -> bytes:
        return b""

    def deserialize_responsibility_assignment(data) -> None:
        return None

    def serialize_responsibility_assignments(objs) -> bytes:
        return b""

    def deserialize_responsibility_assignments(data):
        return []


class ResponsibilityProtoSerializer:
    """Serializer for Responsibility using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: Responsibility | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: Responsibility | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        responsibility = deserialize_responsibility(self.initial_data)
        if responsibility is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = responsibility
        return True

    @beartype
    def save(self) -> Responsibility:
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
        return serialize_responsibility(self.instance)


class ResponsibilityAssignmentProtoSerializer:
    """Serializer for ResponsibilityAssignment using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: ResponsibilityAssignment | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: ResponsibilityAssignment | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        assignment = deserialize_responsibility_assignment(self.initial_data)
        if assignment is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = assignment
        return True

    @beartype
    def save(self) -> ResponsibilityAssignment:
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
        return serialize_responsibility_assignment(self.instance)


class ResponsibilityCollectionProtoSerializer:
    """Serializer for a collection of Responsibility instances using protobuf3."""

    @beartype
    def __init__(self, instances: list[Responsibility] | None = None) -> None:
        self.instances = instances or []

    @beartype
    def data(self) -> bytes | None:
        if not self.instances:
            return None
        return serialize_responsibilities(self.instances)


class ResponsibilityAssignmentCollectionProtoSerializer:
    """Serializer for a collection of ResponsibilityAssignment instances using protobuf3."""

    @beartype
    def __init__(self, instances: list[ResponsibilityAssignment] | None = None) -> None:
        self.instances = instances or []

    @beartype
    def data(self) -> bytes | None:
        if not self.instances:
            return None
        return serialize_responsibility_assignments(self.instances)
