"""
Custom type definitions and type aliases for the reports app.

Centralizes reusable type hints and aliases for report payloads, export
formats, and related data structures, and provides Protocols for report
payload managers, export formatters, and result processors to enable strict
type-safety across modules.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Protocols for report payload managers, export formatters, and result processors

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from typing import Any, List, Protocol, TypedDict, runtime_checkable
from beartype import beartype

class ReportPayloadDict(TypedDict):
    """TypedDict for a report payload."""
    id: str
    report_type: str
    generated_at: str
    data: Any
    author: str
    status: str

class ExportFormatDict(TypedDict):
    """TypedDict for an export format."""
    format: str
    options: dict[str, Any]

class ReportResultDict(TypedDict):
    """TypedDict for a report result."""
    success: bool
    messages: List[str]
    output: Any

@runtime_checkable
class ReportPayloadManager(Protocol):
    """Protocol for managing report payloads."""

    @beartype
    def get_payload(self, report_id: str) -> ReportPayloadDict:
        """Retrieve a report payload by ID.

        Args:
            report_id: The unique identifier for the report.

        Returns:
            ReportPayloadDict: The report payload dictionary.
        """
        ...

    @beartype
    def update_payload(self, report_id: str, data: ReportPayloadDict) -> None:
        """Update a report payload.

        Args:
            report_id: The unique identifier for the report.
            data: The updated report payload dictionary.
        """
        ...

@runtime_checkable
class ExportFormatter(Protocol):
    """Protocol for formatting report exports."""

    @beartype
    def format(
        self,
        payload: ReportPayloadDict,
        export_format: ExportFormatDict,
    ) -> bytes:
        """Format a report payload for export.

        Args:
            payload: The report payload dictionary.
            export_format: The export format dictionary.

        Returns:
            bytes: The formatted export as bytes.
        """
        ...

@runtime_checkable
class ResultProcessor(Protocol):
    """Protocol for processing report results."""

    @beartype
    def process(self, result: ReportResultDict) -> None:
        """Process a report result.

        Args:
            result: The report result dictionary.
        """
        ...
