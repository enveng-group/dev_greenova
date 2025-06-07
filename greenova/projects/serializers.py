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

from typing import Any

from beartype import beartype
from django.core.exceptions import ValidationError

from .models import Project, ProjectMembership

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
        return

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
        instance: Project | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the ProjectProtoSerializer.

        Args:
            instance: Optional Project instance to serialize.
            data: Optional protobuf3 binary data to deserialize.

        """
        self.instance: Project | None = instance
        self.initial_data: bytes | None = data
        self.validated_data: Project | None = None
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
        """Save the validated Project instance to the database.

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
    def data(self) -> bytes | None:
        """Serialize the Project instance to protobuf3 binary format.

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
        instances: list[Project] | None = None,
        data: bytes | None = None,
    ) -> None:
        """Initialize the ProjectCollectionProtoSerializer.

        Args:
            instances: Optional list of Project instances to serialize.
            data: Optional protobuf3 binary data to deserialize.

        """
        self.instances: list[Project] | None = instances
        self.initial_data: bytes | None = data
        self.validated_data: list[Project] | None = None
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
        projects = deserialize_projects(self.initial_data)
        if not projects:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = projects
        return True

    @beartype
    def data(self) -> bytes | None:
        """Serialize the collection of Project instances to protobuf3 binary format.

        Returns:
            Serialized protobuf3 binary data, or None if no instances.

        """
        if self.instances is None:
            return None
        return serialize_projects(self.instances)


class ProjectMembershipProtoSerializer:
    """Serializer for ProjectMembership using protobuf3 binary format."""

    @beartype
    def __init__(
        self,
        instance: ProjectMembership | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data = None
        self.errors = None

    @beartype
    def is_valid(self, raise_exception: bool = False) -> bool:
        from . import projects_pb2  # type: ignore[import]

        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        try:
            proto = projects_pb2.ProjectMembershipProto()  # type: ignore[attr-defined]
            proto.ParseFromString(self.initial_data)
            membership = ProjectMembership().from_pb(proto)
            self.validated_data = membership
            return True
        except Exception as e:
            self.errors = str(e)
            if raise_exception:
                raise ValidationError(self.errors)
            return False

    @beartype
    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        proto = self.instance.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()  # type: ignore[attr-defined]
