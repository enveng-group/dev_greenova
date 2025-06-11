"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Protobuf utilities for mechanism data.

This module provides utility functions for serializing and deserializing data
between Django models and Protocol Buffers for the mechanisms app.
"""

from obligations.models import Obligation
from models import EnvironmentalMechanism
from django.db.models import QuerySet
from typing import cast
from dataclasses import dataclass
import logging
from collections.abc import Sequence


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


def serialize_obligation_insights(
    params: ObligationInsightParams,
) -> ObligationInsightResponse:
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
        insight = response.obligations.add()  # type: ignore
        insight.obligation_number = obligation.obligation_number

        if obligation.action_due_date:
            insight.due_date = obligation.action_due_date.strftime("%Y-%m-%d")

        if obligation.close_out_date:
            insight.close_out_date = obligation.close_out_date.strftime("%Y-%m-%d")

    return response


def serialize_mechanism_chart_data(
    mechanism: EnvironmentalMechanism,
) -> ChartData:
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
        segment = chart_data.segments.add()  # type: ignore
        segment.label = status
        segment.value = value
        segment.color = color

    return chart_data


def serialize_overall_chart_data(
    project_id: int,
    mechanisms: QuerySet,  # QuerySet[EnvironmentalMechanism] if stubs available
) -> ChartData:
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
        segment = chart_data.segments.add()  # type: ignore
        segment.label = status
        segment.value = value
        segment.color = color

    return chart_data


def serialize_chart_response(
    charts: list[ChartData],
    error: str | None = None,
) -> ChartResponse:
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


def status_string_to_enum(status: str) -> ObligationStatus:
    """Convert status string to ObligationStatus enum value.

    Args:
        status: Status string (e.g., "not_started").

    Returns:
        ObligationStatus enum value.

    """
    status_map: dict[str, ObligationStatus] = {
        "not_started": cast("ObligationStatus", ObligationStatus.STATUS_NOT_STARTED),
        "in_progress": cast("ObligationStatus", ObligationStatus.STATUS_IN_PROGRESS),
        "completed": cast("ObligationStatus", ObligationStatus.STATUS_COMPLETED),
        "overdue": cast("ObligationStatus", ObligationStatus.STATUS_OVERDUE),
    }

    return status_map.get(
        status.lower(), cast("ObligationStatus", ObligationStatus.STATUS_UNKNOWN),
    )


def status_enum_to_string(status: ObligationStatus) -> str:
    """Convert ObligationStatus enum value to status string.

    Args:
        status: ObligationStatus enum value.

    Returns:
        Status string (e.g., "not_started").

    """
    status_map: dict[ObligationStatus, str] = {
        cast("ObligationStatus", ObligationStatus.STATUS_NOT_STARTED): "not_started",
        cast("ObligationStatus", ObligationStatus.STATUS_IN_PROGRESS): "in_progress",
        cast("ObligationStatus", ObligationStatus.STATUS_COMPLETED): "completed",
        cast("ObligationStatus", ObligationStatus.STATUS_OVERDUE): "overdue",
    }

    return status_map.get(status, "unknown")
