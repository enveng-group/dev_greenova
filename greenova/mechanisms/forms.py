# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Mechanism logic and state management for the mechanisms app.

This module provides the Mechanism class for managing mechanism definitions
and state, with strict type annotations and runtime type checking.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Mechanism class for definition and state management

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Dict, Any

from beartype import beartype

from .types import MechanismDefinitionDict, MechanismStateDict


class Mechanism:
    """Class for managing mechanism definitions and state."""

    @beartype
    def __init__(self, definition: MechanismDefinitionDict) -> None:
        """
        Initialize a Mechanism with a definition.

        Args:
            definition: MechanismDefinitionDict describing the mechanism.
        """
        self.definition: MechanismDefinitionDict = definition
        self.state: MechanismStateDict = {}

    @beartype
    def initialize(self, initial_state: MechanismStateDict) -> None:
        """
        Initialize the mechanism state.

        Args:
            initial_state: The initial state dictionary for the mechanism.
        """
        self.state = initial_state

    @beartype
    def update_state(self, updates: Dict[str, Any]) -> None:
        """
        Update the mechanism state with new values.

        Args:
            updates: Dictionary of state updates.
        """
        self.state.update(updates)

    @beartype
    def get_state(self) -> MechanismStateDict:
        """
        Get the current mechanism state.

        Returns:
            MechanismStateDict: The current state of the mechanism.
        """
        return self.state
