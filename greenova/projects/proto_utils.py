# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the projects app.

This module provides serialization and deserialization helpers for converting
between Django Project models and Protocol Buffer messages in the projects app.

Features:
    - Safe import and fallback stubs for protobufs
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serialization/deserialization helpers for Project and ProjectCollection

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from typing import Any, List, Optional

from beartype import beartype

from .models import Project
from .types import ProjectMetadataDict, ProjectMembershipDict, ProjectObligationDict

logger = logging.getLogger(__name__)

try:
    from .proto import projects_pb2
except ImportError:
    projects_pb2 = None
    logger.warning("projects_pb2 not found. Ensure .proto files are compiled.")

    class ProjectProto:
        """Stub ProjectProto for missing protobufs."""

        @beartype
        def SerializeToString(self) -> bytes:
            """Serialize the dummy project proto to bytes.

            Returns:
                Empty bytes object.
            """
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            """Parse the dummy project proto from bytes.

            Args:
                data: Bytes to parse (ignored).
            """
            pass

    class ProjectCollection:
        """Stub ProjectCollection for missing protobufs."""

        projects: list[Any] = []

        @beartype
        def SerializeToString(self) -> bytes:
            """Serialize the dummy project collection to bytes.

            Returns:
                Empty bytes object.
            """
            return b""

        @beartype
        def ParseFromString(self, data: bytes) -> None:
            """Parse the dummy project collection from bytes.

            Args:
                data: Bytes to parse (ignored).
            """
            pass

    projects_pb2 = type(
        "projects_pb2",
        (),
        {
            "ProjectProto": ProjectProto,
            "ProjectCollection": ProjectCollection,
        },
    )


@beartype
def serialize_project(project: Project) -> Optional[bytes]:
    """Serialize a Project instance to a Protocol Buffer message.

    Args:
        project: The Project instance to serialize.

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed.

    Raises:
        Exception: For any serialization error.
    """
    try:
        proto = project.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize project: %s", str(e))
        return None


@beartype
def deserialize_project(data: bytes) -> Optional[Project]:
    """Deserialize Protocol Buffer data to a Project instance.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        Project instance, or None if deserialization failed.

    Raises:
        Exception: For any deserialization error.
    """
    try:
        proto = projects_pb2.ProjectProto()
        proto.ParseFromString(data)
        return Project().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception("Failed to deserialize project: %s", str(e))
        return None


@beartype
def serialize_projects(projects: List[Project]) -> Optional[bytes]:
    """Serialize a list of Project instances to a Protocol Buffer collection.

    Args:
        projects: List of Project instances to serialize.

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed.

    Raises:
        Exception: For any serialization error.
    """
    try:
        collection = projects_pb2.ProjectCollection()
        for project in projects:
            proto = project.to_pb()  # type: ignore[attr-defined]
            collection.projects.append(proto)
        return collection.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize projects collection: %s", str(e))
        return None


@beartype
def deserialize_projects(data: bytes) -> List[Project]:
    """Deserialize Protocol Buffer data to a list of Project instances.

    Args:
        data: Serialized protocol buffer data.

    Returns:
        List of Project instances, or empty list if deserialization failed.

    Raises:
        Exception: For any deserialization error.
    """
    try:
        collection = projects_pb2.ProjectCollection()
        collection.ParseFromString(data)
        projects: List[Project] = []
        for proto in getattr(collection, "projects", []):
            project = Project().from_pb(proto)  # type: ignore[attr-defined]
            if project:
                projects.append(project)
        return projects
    except Exception as e:
        logger.exception("Failed to deserialize projects collection: %s", str(e))
        return []
