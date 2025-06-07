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

from beartype import beartype

from .types import ProcedureDefinitionDict, ProcedureResultDict, ProcedureStepDict


@beartype
def parse_procedure_steps(data: str) -> list[ProcedureStepDict]:
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
            msg = "Procedure steps should be a list."
            raise ValueError(msg)
        return steps
    except json.JSONDecodeError as e:
        msg = f"Invalid JSON data: {e}"
        raise ValueError(msg)


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
            msg = "Procedure definition should be a dictionary."
            raise ValueError(msg)
        return definition
    except json.JSONDecodeError as e:
        msg = f"Invalid JSON data: {e}"
        raise ValueError(msg)


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
            msg = "Procedure result should be a dictionary."
            raise ValueError(msg)
        return result
    except json.JSONDecodeError as e:
        msg = f"Invalid JSON data: {e}"
        raise ValueError(msg)
