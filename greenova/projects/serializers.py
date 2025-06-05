# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the projects app.

This module provides serializers for converting between Django Project models
and Protocol Buffer messages using protobuf3 binary format.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serializers for single Project and collections of Projects

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Any, Optional

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import Project
from .types import ProjectMetadataDict, ProjectMembershipDict, ProjectObligationDict

try:
    from .proto_utils import (
        deserialize_project,
        deserialize_projects,
        serialize_project,
        serialize_projects,
    )
except ImportError:

    def serialize_project(obj: Any) -> bytes:
        """Stub serialize_project for missing proto_utils."""
        return b""

    def deserialize_project(data: bytes) -> None:
        """Stub deserialize_project for missing proto_utils."""
        return None

    def serialize_projects(objs: list[Any]) -> bytes:
        """Stub serialize_projects for missing proto_utils."""
        return b""

    def deserialize_projects(data: bytes) -> list[Any]:
        """Stub deserialize_projects for missing proto_utils."""
        return []


class ProjectProtoSerializer:
    """Serializer for Project using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: Optional[Project] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the ProjectProtoSerializer.

        Args:
            instance: Optional Project instance to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instance: Optional[Project] = instance
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[Project] = None
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
        project = deserialize_project(self.initial_data)
        if project is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = project
        return True

    @beartype
    def save(self) -> Project:
        """
        Save the validated Project instance to the database.

        Returns:
            The saved Project instance.

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
        Serialize the Project instance to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instance.
        """
        if self.instance is None:
            return None
        return serialize_project(self.instance)


class ProjectCollectionProtoSerializer:
    """Serializer for a collection of Project instances using protobuf3."""

    @beartype
    def __init__(
        self,
        instances: Optional[list[Project]] = None,
        data: Optional[bytes] = None,
    ) -> None:
        """
        Initialize the ProjectCollectionProtoSerializer.

        Args:
            instances: Optional list of Project instances to serialize.
            data: Optional protobuf3 binary data to deserialize.
        """
        self.instances: Optional[list[Project]] = instances
        self.initial_data: Optional[bytes] = data
        self.validated_data: Optional[list[Project]] = None
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
        projects = deserialize_projects(self.initial_data)
        if not projects:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = projects
        return True

    @beartype
    def data(self) -> Optional[bytes]:
        """
        Serialize the collection of Project instances to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instances.
        """
        if self.instances is None:
            return None
        return serialize_projects(self.instances)
