# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the projects app."""

import logging

from .models import Project

logger = logging.getLogger(__name__)

try:
    from .proto import projects_pb2
except ImportError:
    projects_pb2 = None
    logger.warning("projects_pb2 not found. Ensure .proto files are compiled.")

    class ProjectProto:
        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
            pass

    class ProjectCollection:
        projects = []

        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
            pass

    projects_pb2 = type(
        "projects_pb2",
        (),
        {
            "ProjectProto": ProjectProto,
            "ProjectCollection": ProjectCollection,
        },
    )


def serialize_project(project: Project) -> bytes | None:
    try:
        proto = project.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize project: %s", str(e))
        return None


def deserialize_project(data: bytes) -> Project | None:
    try:
        proto = projects_pb2.ProjectProto()
        proto.ParseFromString(data)
        return Project().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception("Failed to deserialize project: %s", str(e))
        return None


def serialize_projects(projects: list[Project]) -> bytes | None:
    try:
        collection = projects_pb2.ProjectCollection()
        for project in projects:
            proto = project.to_pb()  # type: ignore[attr-defined]
            collection.projects.append(proto)
        return collection.SerializeToString()
    except Exception as e:
        logger.exception("Failed to serialize projects collection: %s", str(e))
        return None


def deserialize_projects(data: bytes) -> list[Project]:
    try:
        collection = projects_pb2.ProjectCollection()
        collection.ParseFromString(data)
        projects = []
        for proto in getattr(collection, "projects", []):
            project = Project().from_pb(proto)  # type: ignore[attr-defined]
            if project:
                projects.append(project)
        return projects
    except Exception as e:
        logger.exception("Failed to deserialize projects collection: %s", str(e))
        return []
