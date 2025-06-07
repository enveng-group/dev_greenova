# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the company app.

This module provides serializers for converting between Django Company models
and Protocol Buffer messages using protobuf3 binary format.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serializers for single Company and collections of Companies

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import Company

try:
    from .proto_utils import (
        deserialize_companies,
        deserialize_company,
        serialize_companies,
        serialize_company,
    )
except ImportError:

    def serialize_company(obj: object) -> bytes:
        """Stub serialize_company for missing proto_utils."""
        return b""

    def deserialize_company(data: bytes) -> None:
        """Stub deserialize_company for missing proto_utils."""
        return

    def serialize_companies(objs: list[object]) -> bytes:
        """Stub serialize_companies for missing proto_utils."""
        return b""

    def deserialize_companies(data: bytes) -> list[object]:
        """Stub deserialize_companies for missing proto_utils."""
        return []


class CompanyProtoSerializer:
    """Serializer for Company using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: Company | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the CompanyProtoSerializer.

        Args:
            instance: Optional Company instance to serialize.
            data: Optional protobuf3 binary data to deserialize.

        """
        self.instance: Company | None = instance
        self.initial_data: bytes | None = data
        self.validated_data: Company | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """Validate the initial protobuf data and populate validated_data.

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
        company = deserialize_company(self.initial_data)
        if company is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = company
        return True

    @beartype
    def save(self) -> Company:
        """Save the validated Company instance to the database.

        Returns:
            The saved Company instance.

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
    def data(self) -> bytes | None:
        """Serialize the Company instance to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instance.

        """
        if self.instance is None:
            return None
        return serialize_company(self.instance)


class CompanyCollectionProtoSerializer:
    """Serializer for a collection of Company instances using protobuf3."""

    @beartype
    def __init__(
        self,
        instances: list[Company] | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the CompanyCollectionProtoSerializer.

        Args:
            instances: Optional list of Company instances to serialize.
            data: Optional protobuf3 binary data to deserialize.

        """
        self.instances: list[Company] | None = instances
        self.initial_data: bytes | None = data
        self.validated_data: list[Company] | None = None
        self.errors: str | None = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        """Validate the initial protobuf data and populate validated_data.

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
        companies = deserialize_companies(self.initial_data)
        if not companies:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = companies
        return True

    @beartype
    def data(self) -> bytes | None:
        """Serialize the collection of Company instances to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instances.

        """
        if self.instances is None:
            return None
        return serialize_companies(self.instances)
