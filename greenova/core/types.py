"""Global type definitions and protocols for Greenova.

These types and protocols are available for use across all apps (dashboard, landing, protobuf, sidebar, navigation, etc).

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Protocol, TypedDict, runtime_checkable


class ProjectMetadataDict(TypedDict):
    """TypedDict for project metadata."""

    id: str
    name: str
    description: str
    member_user_ids: list[str]
    created_at: str
    updated_at: str


class ProjectMembershipDict(TypedDict):
    """TypedDict for project membership."""

    id: str
    project_id: str
    user_id: str
    role: str
    created_at: str
    updated_at: str


class ProjectObligationDict(TypedDict):
    """TypedDict for project obligation relationship."""

    id: str
    project_id: str
    obligation_id: str
    created_at: str
    updated_at: str


@runtime_checkable
class ProjectManager(Protocol):
    ...


@runtime_checkable
class MembershipManager(Protocol):
    ...


@runtime_checkable
class ObligationRelationshipHandler(Protocol):
    ...
