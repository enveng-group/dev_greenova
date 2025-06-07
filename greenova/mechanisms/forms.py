# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Mechanism logic and state management for the mechanisms app.

This module provides the Mechanism class for managing mechanism definitions and
state, with strict type annotations and runtime type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Mechanism class for definition and state management

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""
# Add/complete Google style docstrings for all public classes and methods as needed.

import logging
from typing import Any

import bleach
from beartype import beartype
from core.types import (
    MechanismDefinitionDict,
    MechanismStateDict,
)

logger = logging.getLogger(__name__)


def sanitize_html(value: str) -> str:
    """Sanitize user-supplied HTML/text using bleach.

    Args:
        value: The string to sanitize.

    Returns:
        The sanitized string.

    """
    return bleach.clean(value)


class Mechanism:
    """Class for managing mechanism definitions and state."""

    definition: MechanismDefinitionDict
    state: MechanismStateDict

    @beartype
    def __init__(self, definition: MechanismDefinitionDict) -> None:
        """Initialize a Mechanism with a definition.

        Args:
            definition: MechanismDefinitionDict describing the mechanism.

        """
        self.definition = definition
        # Provide all required fields for MechanismStateDict
        self.state: MechanismStateDict = {
            "id": "",
            "mechanism_id": definition["id"],
            "status": "not_started",
            "last_run": None,
            "result": None,
        }

    @beartype
    def initialize(self, initial_state: MechanismStateDict) -> None:
        """Initialize the mechanism state.

        Args:
            initial_state: The initial state dictionary for the mechanism.

        """
        self.state = initial_state

    @beartype
    def update_state(self, updates: dict[str, Any]) -> None:
        """Update the mechanism state with new values.

        Args:
            updates: Dictionary of state updates.

        """
        for k, v in updates.items():
            if k in self.state:
                self.state[k] = v

    @beartype
    def get_state(self) -> MechanismStateDict:
        """Get the current state of the mechanism.

        Returns:
            The current mechanism state dictionary.

        """
        return self.state
