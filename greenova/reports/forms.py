# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Forms and protocol definitions for the reports app.

This module provides type definitions and protocol interfaces for report
payloads and export formats in the reports app.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for report payload and export format serialization

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

from typing import Protocol, TypedDict

from beartype import beartype


class ReportPayloadDict(TypedDict):
    """TypedDict for report payload data."""

    report_id: str
    user_id: str
    timestamp: str


class ExportFormatDict(TypedDict):
    """TypedDict for export format data."""

    format: str
    options: dict


class ReportPayload(Protocol):
    """Protocol for report payload serialization."""

    @beartype
    def to_dict(self) -> ReportPayloadDict:
        """Convert the report payload to a dictionary.

        Returns:
            ReportPayloadDict: The dictionary representation of the payload.

        """
        ...


class ExportFormat(Protocol):
    """Protocol for export format serialization."""

    @beartype
    def to_dict(self) -> ExportFormatDict:
        """Convert the export format to a dictionary.

        Returns:
            ExportFormatDict: The dictionary representation of the export format.

        """
        ...
