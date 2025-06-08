"""Type definitions for the Greenova core app.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import TypedDict

# Example: Add any shared types or protocols needed by other apps here.


class HTMLSanitizationOptions(TypedDict, total=False):
    allowed_tags: list[str]
    allowed_attributes: dict[str, list[str]]
    strip: bool


class MechanismDefinitionDict(TypedDict, total=False):
    id: str
    name: str
    description: str
    fields: list[str]


class MechanismStateDict(TypedDict, total=False):
    id: str
    state: str
    updated_at: str
