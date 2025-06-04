# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the mechanisms app."""

from django.core.exceptions import ValidationError

from .models import EnvironmentalMechanism

try:
    from .proto_utils import (
        deserialize_mechanism,
        deserialize_mechanisms,
        serialize_mechanism,
        serialize_mechanisms,
    )
except ImportError:

    def serialize_mechanism(obj) -> bytes:
        return b""

    def deserialize_mechanism(data) -> None:
        return None

    def serialize_mechanisms(objs) -> bytes:
        return b""

    def deserialize_mechanisms(data):
        return []


class MechanismProtoSerializer:
    """Serializer for EnvironmentalMechanism using protobuf3 binary format."""

    def __init__(
        self,
        instance: EnvironmentalMechanism | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: EnvironmentalMechanism | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        mechanism = deserialize_mechanism(self.initial_data)
        if mechanism is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = mechanism
        return True

    def save(self) -> EnvironmentalMechanism:
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        return serialize_mechanism(self.instance)


class MechanismCollectionProtoSerializer:
    """Serializer for a collection of EnvironmentalMechanism instances using protobuf3."""

    def __init__(
        self,
        instances: list[EnvironmentalMechanism] | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instances = instances
        self.initial_data = data
        self.validated_data: list[EnvironmentalMechanism] | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        mechanisms = deserialize_mechanisms(self.initial_data)
        if not mechanisms:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = mechanisms
        return True

    def data(self) -> bytes | None:
        if self.instances is None:
            return None
        return serialize_mechanisms(self.instances)
