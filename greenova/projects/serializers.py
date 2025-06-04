# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the projects app."""

from django.core.exceptions import ValidationError

from .models import Project

try:
    from .proto_utils import (
        deserialize_project,
        deserialize_projects,
        serialize_project,
        serialize_projects,
    )
except ImportError:

    def serialize_project(obj) -> bytes:
        return b""

    def deserialize_project(data) -> None:
        return None

    def serialize_projects(objs) -> bytes:
        return b""

    def deserialize_projects(data):
        return []


class ProjectProtoSerializer:
    """Serializer for Project using protobuf3 binary format."""

    def __init__(
        self,
        instance: Project | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: Project | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
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

    def save(self) -> Project:
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        return serialize_project(self.instance)


class ProjectCollectionProtoSerializer:
    """Serializer for a collection of Project instances using protobuf3."""

    def __init__(
        self,
        instances: list[Project] | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instances = instances
        self.initial_data = data
        self.validated_data: list[Project] | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
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

    def data(self) -> bytes | None:
        if self.instances is None:
            return None
        return serialize_projects(self.instances)
