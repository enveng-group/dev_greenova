"""
Custom type definitions and type aliases for the procedures app.

Centralizes reusable type hints and aliases for workflow steps, procedure
definitions, and result types, and provides Protocols for procedure managers,
step evaluators, and result processors to enable strict type-safety across
modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for procedure managers, step evaluators, and result processors

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any, List, Protocol, TypedDict, runtime_checkable
from beartype import beartype

class ProcedureStepDict(TypedDict):
    """TypedDict for a single procedure step."""
    id: str
    name: str
    description: str
    order: int
    completed: bool

class ProcedureDefinitionDict(TypedDict):
    """TypedDict for a procedure definition."""
    id: str
    name: str
    steps: List["ProcedureStepDict"]
    created_at: str
    updated_at: str

class ProcedureResultDict(TypedDict):
    """TypedDict for a procedure result."""
    success: bool
    messages: List[str]
    output: Any

@runtime_checkable
class ProcedureManager(Protocol):
    """Protocol for managing procedures."""

    @beartype
    def get_procedure(self, procedure_id: str) -> ProcedureDefinitionDict:
        """Retrieve a procedure definition by ID.

        Args:
            procedure_id: The unique identifier for the procedure.

        Returns:
            ProcedureDefinitionDict: The procedure definition.
        """
        ...

    @beartype
    def update_procedure(
        self,
        procedure_id: str,
        data: ProcedureDefinitionDict,
    ) -> None:
        """Update a procedure definition.

        Args:
            procedure_id: The unique identifier for the procedure.
            data: The updated procedure definition.
        """
        ...

@runtime_checkable
class StepEvaluator(Protocol):
    """Protocol for evaluating a procedure step."""

    @beartype
    def evaluate(self, step: ProcedureStepDict) -> bool:
        """Evaluate a single procedure step.

        Args:
            step: The procedure step dictionary.

        Returns:
            bool: True if the step is valid/completed, False otherwise.
        """
        ...

@runtime_checkable
class ResultProcessor(Protocol):
    """Protocol for processing procedure results."""

    @beartype
    def process(self, result: ProcedureResultDict) -> None:
        """Process a procedure result.

        Args:
            result: The procedure result dictionary.
        """
        ...
