"""
Custom type definitions and type aliases for the obligations app.

Centralizes reusable type hints and aliases for obligations, compliance
records, and related data structures, and provides Protocols for obligation
data managers, compliance checkers, and status evaluators to enable strict
type-safety across modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for obligation data managers, compliance checkers, and status evaluators

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any, List, Protocol, TypedDict, runtime_checkable
from beartype import beartype

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
    issues: List[str]

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
