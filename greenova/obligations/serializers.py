# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the obligations app.

This module provides serializers for converting between Django Obligation models
and Protocol Buffer messages using protobuf3 binary format.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serializers for single Obligation and collections of Obligations

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Optional, List

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import Obligation
from .types import ObligationDataDict, ComplianceStatusDict

try:
    from .proto_utils import (
        deserialize_obligation,
        deserialize_obligations,
        serialize_obligation,
        serialize_obligations,
    )
except ImportError:
    # Fallbacks for type checking if proto_utils is missing
    def serialize_obligation(obj: object) -> bytes:
        """Stub serialize_obligation for missing proto_utils."""
        return b""

    def deserialize_obligation(data: bytes) -> None:
        """Stub deserialize_obligation for missing proto_utils."""
        return None

    def serialize_obligations(objs: list[object]) -> bytes:
        """Stub serialize_obligations for missing proto_utils."""
        return b""

    def deserialize_obligations(data: bytes) -> list[object]:
        """Stub deserialize_obligations for missing proto_utils."""
        return []


class ObligationProtoSerializer:
    """Serializer for Obligation using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: Optional[Obligation] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the ObligationProtoSerializer.

        Args:
            instance: Optional Obligation instance to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instance: Optional[Obligation] = instance
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[Obligation] = None
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
        obligation = deserialize_obligation(self.initial_data)
        if obligation is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = obligation
        return True

    @beartype
    def save(self) -> Obligation:
        """
        Save the validated Obligation instance to the database.

        Returns:
            The saved Obligation instance.

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
        Serialize the Obligation instance to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instance.
        """
        if self.instance is None:
            return None
        return serialize_obligation(self.instance)


class ObligationCollectionProtoSerializer:
    """Serializer for a collection of Obligation instances using protobuf3."""

    @beartype
    def __init__(
        self,
        instances: Optional[List[Obligation]] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the ObligationCollectionProtoSerializer.

        Args:
            instances: Optional list of Obligation instances to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instances: Optional[List[Obligation]] = instances
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[List[Obligation]] = None
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
        obligations = deserialize_obligations(self.initial_data)
        if not obligations:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = obligations
        return True

    @beartype
    def data(self) -> Optional[bytes]:
        """
        Serialize the collection of Obligation instances to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instances.
        """
        if self.instances is None:
            return None
        return serialize_obligations(self.instances)
