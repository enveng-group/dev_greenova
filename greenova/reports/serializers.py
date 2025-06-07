# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the reports app.

This module provides serializers for converting between Django Report models
and Protocol Buffer messages using protobuf3 binary format.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serializers for single Report and collections of Reports

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Any

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import Report

try:
    from .proto_utils import (
        deserialize_report,
        deserialize_reports,
        serialize_report,
        serialize_reports,
    )
except ImportError:

    def serialize_report(obj: Any) -> bytes:
        """Stub serialize_report for missing proto_utils."""
        return b""

    def deserialize_report(data: bytes) -> None:
        """Stub deserialize_report for missing proto_utils."""
        return

    def serialize_reports(objs: list[Any]) -> bytes:
        """Stub serialize_reports for missing proto_utils."""
        return b""

    def deserialize_reports(data: bytes) -> list[Any]:
        """Stub deserialize_reports for missing proto_utils."""
        return []


class ReportProtoSerializer:
    """Serializer for Report using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: Report | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the ReportProtoSerializer.

        Args:
            instance: Optional Report instance to serialize.
            data: Optional protobuf3 binary data to deserialize.

        """
        self.instance: Report | None = instance
        self.initial_data: bytes | None = data
        self.validated_data: Report | None = None
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
        report = deserialize_report(self.initial_data)
        if report is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = report
        return True

    @beartype
    def save(self) -> Report:
        """Save the validated Report instance to the database.

        Returns:
            The saved Report instance.

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
        """Serialize the Report instance to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instance.

        """
        if self.instance is None:
            return None
        return serialize_report(self.instance)


class ReportCollectionProtoSerializer:
    """Serializer for a collection of Report instances using protobuf3."""

    @beartype
    def __init__(
        self,
        instances: list[Report] | None = None,
    ) -> None:
        """Initialize the ReportCollectionProtoSerializer.

        Args:
            instances: Optional list of Report instances to serialize.

        """
        self.instances: list[Report] = instances or []

    @beartype
    def data(self) -> bytes | None:
        """Serialize the collection of Report instances to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instances.

        """
        if not self.instances:
            return None
        return serialize_reports(self.instances)
