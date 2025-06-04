# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the obligations app."""

from django.core.exceptions import ValidationError

from .models import Obligation

try:
    from .proto_utils import (
        deserialize_obligation,
        deserialize_obligations,
        serialize_obligation,
        serialize_obligations,
    )
except ImportError:
    # Fallbacks for type checking if proto_utils is missing
    def serialize_obligation(obj) -> bytes:
        return b""

    def deserialize_obligation(data) -> None:
        return None

    def serialize_obligations(objs) -> bytes:
        return b""

    def deserialize_obligations(data):
        return []


class ObligationProtoSerializer:
    """Serializer for Obligation using protobuf3 binary format."""

    def __init__(
        self,
        instance: Obligation | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: Obligation | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        obligation = deserialize_obligation(self.initial_data)
        if obligation is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = obligation
        return True

    def save(self) -> Obligation:
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        return serialize_obligation(self.instance)


class ObligationCollectionProtoSerializer:
    """Serializer for a collection of Obligation instances using protobuf3."""

    def __init__(
        self,
        instances: list[Obligation] | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instances = instances
        self.initial_data = data
        self.validated_data: list[Obligation] | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        obligations = deserialize_obligations(self.initial_data)
        if not obligations:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = obligations
        return True

    def data(self) -> bytes | None:
        if self.instances is None:
            return None
        return serialize_obligations(self.instances)
