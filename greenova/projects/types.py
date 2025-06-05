"""
Custom type definitions and type aliases for the projects app.

Centralizes reusable type hints and aliases for project metadata, status, and
relationships, and provides Protocols for project managers, membership
managers, and obligation relationship handlers to enable strict type-safety
across modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for project managers, membership managers, and obligation relationship handlers

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import List, Protocol, TypedDict, runtime_checkable
from beartype import beartype

class ProjectMetadataDict(TypedDict):
    """TypedDict for project metadata."""
    id: str
    name: str
    description: str
    member_user_ids: List[str]
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
    """Protocol for managing projects."""

    @beartype
    def get_project(self, project_id: str) -> ProjectMetadataDict:
        """Retrieve a project by ID.

        Args:
            project_id: The unique identifier for the project.

        Returns:
            ProjectMetadataDict: The project metadata dictionary.
        """
        ...

    @beartype
    def update_project(self, project_id: str, data: ProjectMetadataDict) -> None:
        """Update a project.

        Args:
            project_id: The unique identifier for the project.
            data: The updated project metadata dictionary.
        """
        ...

@runtime_checkable
class MembershipManager(Protocol):
    """Protocol for managing project memberships."""

    @beartype
    def add_member(self, project_id: str, user_id: str, role: str) -> None:
        """Add a member to a project.

        Args:
            project_id: The project ID.
            user_id: The user ID.
            role: The role to assign.
        """
        ...

    @beartype
    def remove_member(self, project_id: str, user_id: str) -> None:
        """Remove a member from a project.

        Args:
            project_id: The project ID.
            user_id: The user ID.
        """
        ...

    @beartype
    def list_members(self, project_id: str) -> List[ProjectMembershipDict]:
        """List all members of a project.

        Args:
            project_id: The project ID.

        Returns:
            List[ProjectMembershipDict]: List of project membership dictionaries.
        """
        ...

@runtime_checkable
class ObligationRelationshipHandler(Protocol):
    """Protocol for managing project-obligation relationships."""

    @beartype
    def link_obligation(self, project_id: str, obligation_id: str) -> None:
        """Link an obligation to a project.

        Args:
            project_id: The project ID.
            obligation_id: The obligation ID.
        """
        ...

    @beartype
    def unlink_obligation(self, project_id: str, obligation_id: str) -> None:
        """Unlink an obligation from a project.

        Args:
            project_id: The project ID.
            obligation_id: The obligation ID.
        """
        ...

    @beartype
    def list_obligations(self, project_id: str) -> List[ProjectObligationDict]:
        """List all obligations linked to a project.

        Args:
            project_id: The project ID.

        Returns:
            List[ProjectObligationDict]: List of project-obligation dictionaries.
        """
        ...
