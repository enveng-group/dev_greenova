# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Type definitions and protocol interfaces for the procedures app.

This module provides type definitions and protocol interfaces for procedure
steps and definitions in the procedures app.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for procedure step and definition serialization

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Protocol, TypedDict, List, Optional

from beartype import beartype


class ProcedureStepDict(TypedDict):
    """TypedDict for a single procedure step."""
    id: int
    name: str
    description: Optional[str]


class ProcedureDefinitionDict(TypedDict):
    """TypedDict for a procedure definition."""
    id: int
    name: str
    steps: List[ProcedureStepDict]


class ProcedureStep(Protocol):
    """Protocol for procedure step serialization."""

    @beartype
    def to_dict(self) -> ProcedureStepDict:
        """
        Convert the procedure step to a dictionary.

        Returns:
            ProcedureStepDict: The dictionary representation of the step.
        """
        ...


class ProcedureDefinition(Protocol):
    """Protocol for procedure definition serialization."""

    @beartype
    def to_dict(self) -> ProcedureDefinitionDict:
        """
        Convert the procedure definition to a dictionary.

        Returns:
            ProcedureDefinitionDict: The dictionary representation of the definition.
        """
        ...
