"""
Custom type definitions and type aliases for the mechanisms app.

Centralizes reusable type hints and aliases for mechanism definitions, state,
and results, and provides Protocols for mechanism definition managers, state
evaluators, and result processors to enable strict type-safety across modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for mechanism definition managers, state evaluators, and result processors

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any, List, Protocol, TypedDict, runtime_checkable
from beartype import beartype

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
    messages: List[str]
    output: Any

@runtime_checkable
class MechanismDefinitionManager(Protocol):
    """Protocol for managing mechanism definitions."""

    @beartype
    def get_definition(self, mechanism_id: str) -> MechanismDefinitionDict:
        """Retrieve a mechanism definition by ID.

        Args:
            mechanism_id: The unique identifier for the mechanism.

        Returns:
            MechanismDefinitionDict: The mechanism definition dictionary.
        """
        ...

    @beartype
    def update_definition(
        self,
        mechanism_id: str,
        data: MechanismDefinitionDict,
    ) -> None:
        """Update a mechanism definition.

        Args:
            mechanism_id: The unique identifier for the mechanism.
            data: The updated mechanism definition dictionary.
        """
        ...

@runtime_checkable
class MechanismStateEvaluator(Protocol):
    """Protocol for evaluating mechanism state."""

    @beartype
    def evaluate(self, state: MechanismStateDict) -> MechanismResultDict:
        """Evaluate a mechanism state.

        Args:
            state: The mechanism state dictionary.

        Returns:
            MechanismResultDict: The result of the evaluation.
        """
        ...

@runtime_checkable
class MechanismResultProcessor(Protocol):
    """Protocol for processing mechanism results."""

    @beartype
    def process(self, result: MechanismResultDict) -> None:
        """Process a mechanism result.

        Args:
            result: The mechanism result dictionary.
        """
        ...
