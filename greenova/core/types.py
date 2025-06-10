"""Type definitions for the Greenova core app.

This module contains shared type definitions and protocols for use throughout
Greenova. All types here are intended for cross-app and cross-module use.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

# Copyright (c) 2025 Adrian Gallo <agallo@enveng-group.com.au>
# SPDX-License-Identifier: AGPL-3.0

from typing import TypedDict

__all__ = [
    "HTMLSanitizationOptions",
    "MechanismDefinitionDict",
    "MechanismStateDict",
]

# Example: Add any shared types or protocols needed by other apps here.


class HTMLSanitizationOptions(TypedDict, total=False):
    """Options for HTML sanitization.

    Attributes:
        allowed_tags: List of allowed HTML tags.
        allowed_attributes: Mapping of tag names to lists of allowed attributes.
        strip: Whether to strip disallowed tags/attributes (True) or escape them (False).

    """

    allowed_tags: list[str]
    allowed_attributes: dict[str, list[str]]
    strip: bool


class MechanismDefinitionDict(TypedDict, total=False):
    """Definition dictionary for mechanisms.

    Attributes:
        id: Unique identifier for the mechanism.
        name: Human-readable name of the mechanism.
        description: Description of the mechanism's purpose.
        fields: List of field names associated with the mechanism.

    """

    id: str
    name: str
    description: str
    fields: list[str]


class MechanismStateDict(TypedDict, total=False):
    """State dictionary for a mechanism instance.

    Attributes:
        id: Unique identifier for the mechanism instance.
        state: Current state or status string.
        updated_at: ISO 8601 timestamp of last update.

    """

    id: str
    state: str
    updated_at: str
