# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the procedures app."""

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import Procedure

try:
    from .proto_utils import (
        deserialize_procedure,
        deserialize_procedures,
        serialize_procedure,
        serialize_procedures,
    )
except ImportError:

    def serialize_procedure(obj) -> bytes:
        return b""

    def deserialize_procedure(data) -> None:
        return None

    def serialize_procedures(objs) -> bytes:
        return b""

    def deserialize_procedures(data):
        return []


class ProcedureProtoSerializer:
    """Serializer for Procedure using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: Procedure | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: Procedure | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        procedure = deserialize_procedure(self.initial_data)
        if procedure is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = procedure
        return True

    @beartype
    def save(self) -> Procedure:
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
        return serialize_procedure(self.instance)


class ProcedureCollectionProtoSerializer:
    """Serializer for a collection of Procedure instances using protobuf3."""

    @beartype
    def __init__(self, instances: list[Procedure] | None = None) -> None:
        self.instances = instances or []

    @beartype
    def data(self) -> bytes | None:
        if not self.instances:
            return None
        return serialize_procedures(self.instances)
