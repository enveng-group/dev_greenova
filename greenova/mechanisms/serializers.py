# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the mechanisms app.

This module provides serializers for converting between Django
EnvironmentalMechanism models and Protocol Buffer messages using protobuf3
binary format.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serializers for single EnvironmentalMechanism and collections of them

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Optional, List

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import EnvironmentalMechanism
from .types import MechanismDefinitionDict, MechanismStateDict

try:
    from .proto_utils import (
        deserialize_mechanism,
        deserialize_mechanisms,
        serialize_mechanism,
        serialize_mechanisms,
    )
except ImportError:

    def serialize_mechanism(obj: object) -> bytes:
        """Stub serialize_mechanism for missing proto_utils."""
        return b""

    def deserialize_mechanism(data: bytes) -> None:
        """Stub deserialize_mechanism for missing proto_utils."""
        return None

    def serialize_mechanisms(objs: list[object]) -> bytes:
        """Stub serialize_mechanisms for missing proto_utils."""
        return b""

    def deserialize_mechanisms(data: bytes) -> list[object]:
        """Stub deserialize_mechanisms for missing proto_utils."""
        return []


class MechanismProtoSerializer:
    """Serializer for EnvironmentalMechanism using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: Optional[EnvironmentalMechanism] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the MechanismProtoSerializer.

        Args:
            instance: Optional EnvironmentalMechanism instance to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instance: Optional[EnvironmentalMechanism] = instance
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[EnvironmentalMechanism] = None
        self.errors: Optional[str] = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """
        Validate the initial protobuf data and populate validated_data.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.
        """
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

    @beartype
    def save(self) -> EnvironmentalMechanism:
        """
        Save the validated EnvironmentalMechanism instance to the database.

        Returns:
            The saved EnvironmentalMechanism instance.

        Raises:
            ValidationError: If called before is_valid().
        """
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    @beartype
    def data(self) -> Optional[bytes]:
        """
        Serialize the EnvironmentalMechanism instance to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instance.
        """
        if self.instance is None:
            return None
        return serialize_mechanism(self.instance)


class MechanismCollectionProtoSerializer:
    """Serializer for a collection of EnvironmentalMechanism instances using protobuf3."""

    @beartype
    def __init__(
        self,
        instances: Optional[List[EnvironmentalMechanism]] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the MechanismCollectionProtoSerializer.

        Args:
            instances: Optional list of EnvironmentalMechanism instances to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instances: Optional[List[EnvironmentalMechanism]] = instances
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[List[EnvironmentalMechanism]] = None
        self.errors: Optional[str] = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """
        Validate the initial protobuf data and populate validated_data.

        Args:
            raise_exception: Whether to raise ValidationError on failure.

        Returns:
            True if data is valid, False otherwise.

        Raises:
            ValidationError: If data is invalid and raise_exception is True.
        """
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

    @beartype
    def data(self) -> Optional[bytes]:
        """
        Serialize the collection of EnvironmentalMechanism instances to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instances.
        """
        if self.instances is None:
            return None
        return serialize_mechanisms(self.instances)
