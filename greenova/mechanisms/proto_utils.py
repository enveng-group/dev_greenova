# Copyright 2025 Adrian Gallo.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf utilities for mechanism data.

This module provides utility functions for serializing and deserializing data
between Django models and Protocol Buffers for the mechanisms app.

Features:
    - Strict type annotations and runtime type checking with beartype
    - Google style docstrings throughout
    - Serialization/deserialization helpers for mechanism chart and insight data

Author:
    Adrian Gallo <agallo@enveng-group.com.au>
"""

import logging
from dataclasses import dataclass
from typing import Any, cast
from collections.abc import Sequence

from beartype import beartype
from django.db.models import QuerySet

from obligations.models import Obligation
from .models import EnvironmentalMechanism
from .types import MechanismDefinitionDict, MechanismStateDict

# Import protobufs with fallback stubs if needed
try:
    from .proto import (
        ObligationInsightResponse,
        ChartData,
        ChartResponse,
        ObligationStatus,
    )
except ImportError:
    # Fallback stubs for type checking and runtime
    class ObligationInsightResponse:
        @beartype
        def __init__(self) -> None:
            self.mechanism_id: int = 0
            self.status: str = ""
            self.status_key: str = ""
            self.count: int = 0
            self.total_count: int = 0
            self.error: str = ""
            self.obligations: list[Any] = []

        @beartype
        def obligations_add(self) -> Any:
            obligation = type("ObligationInsight", (), {})()
            self.obligations.append(obligation)
            return obligation

        def obligations(self) -> Any:
            return self.obligations

    class ChartData:
        @beartype
        def __init__(self) -> None:
            self.mechanism_id: int = 0
            self.mechanism_name: str = ""
            self.segments: list[Any] = []

        @beartype
        def segments_add(self) -> Any:
            segment = type("ChartSegment", (), {})()
            self.segments.append(segment)
            return segment

        def segments(self) -> Any:
            return self.segments

    class ChartResponse:
        @beartype
        def __init__(self) -> None:
            self.charts: list[Any] = []
            self.error: str = ""

    class ObligationStatus:
        STATUS_NOT_STARTED = 0
        STATUS_IN_PROGRESS = 1
        STATUS_COMPLETED = 2
        STATUS_OVERDUE = 3
        STATUS_UNKNOWN = 4

logger = logging.getLogger(__name__)


@dataclass
class ObligationInsightParams:
    """Parameters for obligation insight serialization."""

    mechanism_id: int
    status: str
    status_key: str
    obligations: Sequence[Obligation]
    total_count: int
    error: str | None = None


@beartype
def serialize_obligation_insights(
    params: ObligationInsightParams,
) -> Any:
    """Serialize obligation data to protobuf for chart tooltips.

    Args:
        params: ObligationInsightParams dataclass containing all parameters.

    Returns:
        ObligationInsightResponse protobuf message.
    """
    response = ObligationInsightResponse()
    response.mechanism_id = params.mechanism_id
    response.status = params.status
    response.status_key = params.status_key
    response.count = len(params.obligations)
    response.total_count = params.total_count

    if params.error:
        response.error = params.error
        return response

    for obligation in params.obligations:
        # Use .add() if available, else fallback to obligations_add stub
        if hasattr(response.obligations, "add"):
            insight = response.obligations.add()  # type: ignore
        else:
            insight = response.obligations_add()
        insight.obligation_number = obligation.obligation_number

        if obligation.action_due_date:
            insight.due_date = obligation.action_due_date.strftime("%Y-%m-%d")

        if obligation.close_out_date:
            insight.close_out_date = obligation.close_out_date.strftime("%Y-%m-%d")

    return response


@beartype
def serialize_mechanism_chart_data(
    mechanism: EnvironmentalMechanism,
) -> Any:
    """Serialize mechanism data to protobuf for chart rendering.

    Args:
        mechanism: EnvironmentalMechanism object.

    Returns:
        ChartData protobuf message.
    """
    chart_data = ChartData()
    chart_data.mechanism_id = mechanism.id
    chart_data.mechanism_name = mechanism.name

    # Create chart segments for each status
    statuses: list[str] = ["Not Started", "In Progress", "Completed", "Overdue"]
    values: list[int] = [
        mechanism.not_started_count,
        mechanism.in_progress_count,
        mechanism.completed_count,
        mechanism.overdue_count,
    ]
    colors: list[str] = ["#f9c74f", "#90be6d", "#43aa8b", "#f94144"]

    for status, value, color in zip(statuses, values, colors, strict=False):
        if hasattr(chart_data.segments, "add"):
            segment = chart_data.segments.add()  # type: ignore
        else:
            segment = chart_data.segments_add()
        segment.label = status
        segment.value = value
        segment.color = color

    return chart_data


@beartype
def serialize_overall_chart_data(
    project_id: int,
    mechanisms: QuerySet,  # QuerySet[EnvironmentalMechanism] if stubs available
) -> Any:
    """Serialize overall project data to protobuf for chart rendering.

    Args:
        project_id: ID of the project.
        mechanisms: QuerySet of EnvironmentalMechanism objects.

    Returns:
        ChartData protobuf message.
    """
    chart_data = ChartData()
    chart_data.mechanism_id = 0  # 0 indicates overall chart
    chart_data.mechanism_name = "Overall Status"

    # Aggregate data
    not_started: int = sum(m.not_started_count for m in mechanisms)
    in_progress: int = sum(m.in_progress_count for m in mechanisms)
    completed: int = sum(m.completed_count for m in mechanisms)
    overdue: int = sum(m.overdue_count for m in mechanisms)

    statuses: list[str] = ["Not Started", "In Progress", "Completed", "Overdue"]
    values: list[int] = [not_started, in_progress, completed, overdue]
    colors: list[str] = ["#f9c74f", "#90be6d", "#43aa8b", "#f94144"]

    for status, value, color in zip(statuses, values, colors, strict=False):
        if hasattr(chart_data.segments, "add"):
            segment = chart_data.segments.add()  # type: ignore
        else:
            segment = chart_data.segments_add()
        segment.label = status
        segment.value = value
        segment.color = color

    return chart_data


@beartype
def serialize_chart_response(
    charts: list[Any],
    error: str | None = None,
) -> Any:
    """Serialize chart data to protobuf response.

    Args:
        charts: List of ChartData messages.
        error: Optional error message.

    Returns:
        ChartResponse protobuf message.
    """
    response = ChartResponse()

    if error:
        response.error = error
        return response

    for chart in charts:
        response.charts.append(chart)

    return response


@beartype
def status_string_to_enum(status: str) -> Any:
    """Convert status string to ObligationStatus enum value.

    Args:
        status: Status string (e.g., "not_started").

    Returns:
        ObligationStatus enum value.
    """
    status_map: dict[str, Any] = {
        "not_started": cast("ObligationStatus", ObligationStatus.STATUS_NOT_STARTED),
        "in_progress": cast("ObligationStatus", ObligationStatus.STATUS_IN_PROGRESS),
        "completed": cast("ObligationStatus", ObligationStatus.STATUS_COMPLETED),
        "overdue": cast("ObligationStatus", ObligationStatus.STATUS_OVERDUE),
    }

    return status_map.get(
        status.lower(), cast("ObligationStatus", ObligationStatus.STATUS_UNKNOWN),
    )


@beartype
def status_enum_to_string(status: Any) -> str:
    """Convert ObligationStatus enum value to status string.

    Args:
        status: ObligationStatus enum value.

    Returns:
        Status string (e.g., "not_started").
    """
    status_map: dict[Any, str] = {
        cast("ObligationStatus", ObligationStatus.STATUS_NOT_STARTED): "not_started",
        cast("ObligationStatus", ObligationStatus.STATUS_IN_PROGRESS): "in_progress",
        cast("ObligationStatus", ObligationStatus.STATUS_COMPLETED): "completed",
        cast("ObligationStatus", ObligationStatus.STATUS_OVERDUE): "overdue",
    }

    return status_map.get(status, "unknown")
