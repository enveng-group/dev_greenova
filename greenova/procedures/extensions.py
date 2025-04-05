# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

from __future__ import annotations

import typing


def format_procedure_name(name: str) -> str:
    """Convert procedure name to a more readable format."""
    return name.replace('_', ' ').title()

def format_procedure_status(status: str) -> str:
    """Format procedure status with appropriate styling."""
    statuses = {
        'not started': 'Not Started',
        'in progress': 'In Progress',
        'completed': 'Completed',
        'on hold': 'On Hold'
    }
    return statuses.get(status.lower(), status)

# Dictionary of all filters to be registered
procedure_filters = {
    'format_procedure_name': format_procedure_name,
    'format_procedure_status': format_procedure_status,
}

# Dictionary of all global functions to be registered
procedure_globals: dict[str, typing.Callable] = {
    # Add any global functions here
}
