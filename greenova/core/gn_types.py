"""Global type definitions and protocols for Greenova.

These types and protocols are available for use across all apps (dashboard, landing, protobuf, sidebar, navigation, etc).

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any, Protocol, TypedDict, runtime_checkable

from beartype import beartype


class ProjectMetadataDict(TypedDict):
    """TypedDict for project metadata."""

    id: str
    name: str
    description: str
    created_at: str
    updated_at: str


class ProjectMembershipDict(TypedDict):
    """TypedDict for project membership."""

    user_id: str
    project_id: str
    role: str
    joined_at: str


class ProjectObligationDict(TypedDict):
    """TypedDict for project obligation relationship."""

    id: str
    project_id: str
    obligation_id: str
    created_at: str
    updated_at: str


class ObligationDataDict(TypedDict, total=False):
    """TypedDict for obligation data."""

    obligation_number: str
    project: str
    primary_environmental_mechanism: str | None
    procedure: str
    environmental_aspect: str
    obligation: str
    accountability: str
    responsibility: str
    project_phase: str
    action_due_date: str | None
    close_out_date: str | None
    status: str
    supporting_information: str
    general_comments: str
    compliance_comments: str
    non_conformance_comments: str
    evidence_notes: str
    recurring_obligation: bool
    recurring_frequency: str
    recurring_status: str
    recurring_forecasted_date: str | None
    inspection: bool
    inspection_frequency: str
    site_or_desktop: str
    gap_analysis: bool
    notes_for_gap_analysis: str


class ComplianceStatusDict(TypedDict):
    """TypedDict for compliance status."""

    is_compliant: bool
    issues: list[str]


class MechanismDefinitionDict(TypedDict):
    """TypedDict for a mechanism definition."""

    id: str
    name: str
    description: str
    type: str
    parameters: dict[str, Any]


class MechanismStateDict(TypedDict):
    """TypedDict for a mechanism state."""

    id: str
    mechanism_id: str
    status: str
    last_run: str | None
    result: Any


class MechanismResultDict(TypedDict):
    """TypedDict for a mechanism result."""

    success: bool
    messages: list[str]
    output: Any


@runtime_checkable
class ProjectManager(Protocol):
    ...


@runtime_checkable
class MembershipManager(Protocol):
    ...


@runtime_checkable
class ObligationRelationshipHandler(Protocol):
    ...


@runtime_checkable
class ObligationDataManager(Protocol):
    """Protocol for managing obligation data."""

    @beartype
    def get_obligation(self, obligation_id: str) -> ObligationDataDict:
        """Retrieve an obligation by ID.

        Args:
            obligation_id: The unique identifier for the obligation.

        Returns:
            ObligationDataDict: The obligation data dictionary.

        """
        ...

    @beartype
    def update_obligation(self, obligation_id: str, data: ObligationDataDict) -> None:
        """Update an obligation.

        Args:
            obligation_id: The unique identifier for the obligation.
            data: The updated obligation data dictionary.

        """
        ...


@runtime_checkable
class ComplianceChecker(Protocol):
    """Protocol for checking compliance of an obligation."""

    @beartype
    def check(self, obligation: ObligationDataDict) -> ComplianceStatusDict:
        """Check compliance for an obligation.

        Args:
            obligation: The obligation data dictionary.

        Returns:
            ComplianceStatusDict: The compliance status dictionary.

        """
        ...


@runtime_checkable
class StatusEvaluator(Protocol):
    """Protocol for evaluating obligation status."""

    @beartype
    def evaluate(self, status: str) -> bool:
        """Evaluate the status of an obligation.

        Args:
            status: The status string to evaluate.

        Returns:
            bool: True if the status is valid, False otherwise.

        """
        ...


@runtime_checkable
class MechanismDefinitionManager(Protocol):
    """Protocol for managing mechanism definitions."""

    @beartype
    def get_definition(self, mechanism_id: str) -> MechanismDefinitionDict: ...
    @beartype
    def list_definitions(self) -> list[MechanismDefinitionDict]: ...


@runtime_checkable
class MechanismStateEvaluator(Protocol):
    """Protocol for evaluating mechanism state."""

    @beartype
    def evaluate(self, state: MechanismStateDict) -> MechanismResultDict: ...


@runtime_checkable
class MechanismResultProcessor(Protocol):
    """Protocol for processing mechanism results."""

    @beartype
    def process(self, result: MechanismResultDict) -> None: ...


@runtime_checkable
class ProjectLike(Protocol):
    """Protocol for project-like objects."""

    id: Any
    name: str
    description: str
    created_at: Any
    updated_at: Any
