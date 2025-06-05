# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer and JSON utilities for the procedures app.

This module provides helpers for parsing and validating procedure steps,
definitions, and results from JSON strings, with strict type annotations
and runtime type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Parsing helpers for ProcedureStepDict, ProcedureDefinitionDict, ProcedureResultDict

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import json
from typing import Any, List

from beartype import beartype

from .types import ProcedureStepDict, ProcedureDefinitionDict, ProcedureResultDict


@beartype
def parse_procedure_steps(data: str) -> List[ProcedureStepDict]:
    """Parse a JSON string into a list of procedure steps.

    Args:
        data: JSON string representing a list of procedure steps.

    Returns:
        List of ProcedureStepDict objects.

    Raises:
        ValueError: If the JSON is invalid or not a list.
    """
    try:
        steps = json.loads(data)
        if not isinstance(steps, list):
            raise ValueError("Procedure steps should be a list.")
        return steps
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON data: {e}")


@beartype
def parse_procedure_definition(data: str) -> ProcedureDefinitionDict:
    """Parse a JSON string into a procedure definition dictionary.

    Args:
        data: JSON string representing a procedure definition.

    Returns:
        ProcedureDefinitionDict object.

    Raises:
        ValueError: If the JSON is invalid or not a dictionary.
    """
    try:
        definition = json.loads(data)
        if not isinstance(definition, dict):
            raise ValueError("Procedure definition should be a dictionary.")
        return definition
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON data: {e}")


@beartype
def parse_procedure_result(data: str) -> ProcedureResultDict:
    """Parse a JSON string into a procedure result dictionary.

    Args:
        data: JSON string representing a procedure result.

    Returns:
        ProcedureResultDict object.

    Raises:
        ValueError: If the JSON is invalid or not a dictionary.
    """
    try:
        result = json.loads(data)
        if not isinstance(result, dict):
            raise ValueError("Procedure result should be a dictionary.")
        return result
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON data: {e}")
