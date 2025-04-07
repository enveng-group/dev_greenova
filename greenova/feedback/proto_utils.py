# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""
Utilities for Protocol Buffer serialization in the feedback app.

This module provides functions to convert between Django models and Protocol Buffers.
"""

import datetime
import logging
from typing import List, Optional

from django.contrib.auth import get_user_model
from django.utils import timezone
from google.protobuf import symbol_database as _symbol_database

from .models import BugReport

logger = logging.getLogger(__name__)

# Get the global symbol database
_sym_db = _symbol_database.Default()

# Get message classes from the symbol database
BugReportProto = _sym_db.GetSymbol('feedback.BugReportProto')
BugReportCollection = _sym_db.GetSymbol('feedback.BugReportCollection')


def django_to_proto(bug_report: BugReport) -> BugReportProto:
    """
    Convert a Django BugReport model instance to a Protocol Buffer message.

    Args:
        bug_report: The Django model instance to convert

    Returns:
        A BugReportProto message containing the serialized data
    """
    proto = BugReportProto()

    # Core identifiers
    proto.id = bug_report.id if bug_report.id else 0
    proto.title = bug_report.title
    proto.description = bug_report.description

    # Environment information
    proto.application_version = bug_report.application_version
    proto.operating_system = bug_report.operating_system
    proto.browser = bug_report.browser or ""
    proto.device_type = bug_report.device_type

    # Problem details
    proto.steps_to_reproduce = bug_report.steps_to_reproduce
    proto.expected_behavior = bug_report.expected_behavior
    proto.actual_behavior = bug_report.actual_behavior

    # Technical details
    proto.error_messages = bug_report.error_messages or ""
    proto.trace_report = bug_report.trace_report or ""

    # Frequency and impact
    frequency_map = {
        'always': BugReportProto.Frequency.ALWAYS,
        'frequently': BugReportProto.Frequency.FREQUENTLY,
        'occasionally': BugReportProto.Frequency.OCCASIONALLY,
        'rarely': BugReportProto.Frequency.RARELY
    }
    proto.frequency = frequency_map.get(
        bug_report.frequency, BugReportProto.Frequency.UNKNOWN
    )

    severity_map = {
        'low': BugReportProto.Severity.LOW,
        'medium': BugReportProto.Severity.MEDIUM,
        'high': BugReportProto.Severity.HIGH,
        'critical': BugReportProto.Severity.CRITICAL
    }
    proto.impact_severity = severity_map.get(
        bug_report.impact_severity, BugReportProto.Severity.UNDEFINED
    )
    proto.admin_severity = severity_map.get(
        bug_report.severity, BugReportProto.Severity.UNDEFINED
    )
    proto.user_impact = bug_report.user_impact

    # Additional information
    proto.workarounds = bug_report.workarounds or ""
    proto.additional_comments = bug_report.additional_comments or ""

    # Meta information
    if bug_report.created_by:
        proto.user_id = bug_report.created_by.id
        proto.username = bug_report.created_by.username

    # Convert datetime to timestamp (seconds since epoch)
    if bug_report.created_at:
        proto.created_at = int(bug_report.created_at.timestamp())
    if bug_report.updated_at:
        proto.updated_at = int(bug_report.updated_at.timestamp())

    # Admin fields
    proto.github_issue_url = bug_report.github_issue_url or ""

    status_map = {
        'open': BugReportProto.Status.OPEN,
        'in_progress': BugReportProto.Status.IN_PROGRESS,
        'resolved': BugReportProto.Status.RESOLVED,
        'closed': BugReportProto.Status.CLOSED,
        'rejected': BugReportProto.Status.REJECTED
    }
    proto.status = status_map.get(bug_report.status, BugReportProto.Status.UNSPECIFIED)
    proto.admin_comment = bug_report.admin_comment or ""

    return proto


def proto_to_django(
    proto: BugReportProto,
    instance: Optional[BugReport] = None
) -> BugReport:
    """
    Convert a Protocol Buffer message to a Django BugReport model instance.

    Args:
        proto: The Protocol Buffer message to convert
        instance: Optional existing BugReport instance to update (for updates)

    Returns:
        A BugReport model instance (either new or updated)
    """
    User = get_user_model()

    # Create a new instance or use the provided one
    bug_report = instance or BugReport()

    # Skip ID if creating a new instance (let Django handle it)
    if instance and proto.id:
        bug_report.id = proto.id  # Only set ID for existing instances

    # Core identifiers
    bug_report.title = proto.title
    bug_report.description = proto.description

    # Environment information
    bug_report.application_version = proto.application_version
    bug_report.operating_system = proto.operating_system
    bug_report.browser = proto.browser
    bug_report.device_type = proto.device_type

    # Problem details
    bug_report.steps_to_reproduce = proto.steps_to_reproduce
    bug_report.expected_behavior = proto.expected_behavior
    bug_report.actual_behavior = proto.actual_behavior

    # Technical details
    bug_report.error_messages = proto.error_messages
    bug_report.trace_report = proto.trace_report

    # Frequency and impact
    frequency_map = {
        BugReportProto.Frequency.ALWAYS: 'always',
        BugReportProto.Frequency.FREQUENTLY: 'frequently',
        BugReportProto.Frequency.OCCASIONALLY: 'occasionally',
        BugReportProto.Frequency.RARELY: 'rarely'
    }
    bug_report.frequency = frequency_map.get(proto.frequency, 'rarely')

    severity_map = {
        BugReportProto.Severity.LOW: 'low',
        BugReportProto.Severity.MEDIUM: 'medium',
        BugReportProto.Severity.HIGH: 'high',
        BugReportProto.Severity.CRITICAL: 'critical'
    }
    bug_report.impact_severity = severity_map.get(proto.impact_severity, 'medium')
    bug_report.severity = severity_map.get(proto.admin_severity, 'medium')
    bug_report.user_impact = proto.user_impact

    # Additional information
    bug_report.workarounds = proto.workarounds
    bug_report.additional_comments = proto.additional_comments

    # Meta information
    if proto.user_id:
        try:
            bug_report.created_by = User.objects.get(id=proto.user_id)
        except User.DoesNotExist:
            logger.warning(
                "User with ID %d from protobuf message not found",
                proto.user_id
            )

    # Convert timestamps to datetime objects
    if proto.created_at:
        bug_report.created_at = datetime.datetime.fromtimestamp(
            proto.created_at, tz=timezone.get_current_timezone()
        )
    if proto.updated_at:
        bug_report.updated_at = datetime.datetime.fromtimestamp(
            proto.updated_at, tz=timezone.get_current_timezone()
        )

    # Admin fields
    bug_report.github_issue_url = proto.github_issue_url

    status_map = {
        BugReportProto.Status.OPEN: 'open',
        BugReportProto.Status.IN_PROGRESS: 'in_progress',
        BugReportProto.Status.RESOLVED: 'resolved',
        BugReportProto.Status.CLOSED: 'closed',
        BugReportProto.Status.REJECTED: 'rejected'
    }
    bug_report.status = status_map.get(proto.status, 'open')
    bug_report.admin_comment = proto.admin_comment

    return bug_report


def serialize_bug_reports(bug_reports: List[BugReport]) -> bytes:
    """
    Serialize a list of BugReport instances to a binary Protocol Buffer message.

    Args:
        bug_reports: List of Django BugReport model instances

    Returns:
        Binary serialized data
    """
    collection = BugReportCollection()
    for report in bug_reports:
        proto = django_to_proto(report)
        collection.reports.append(proto)

    return collection.SerializeToString()


def deserialize_bug_reports(binary_data: bytes) -> List[BugReport]:
    """
    Deserialize binary Protocol Buffer data to a list of BugReport instances.

    Args:
        binary_data: Binary serialized data

    Returns:
        List of Django BugReport model instances
    """
    collection = BugReportCollection()
    collection.ParseFromString(binary_data)

    return [proto_to_django(proto) for proto in collection.reports]


def serialize_bug_report(bug_report: BugReport) -> bytes:
    """
    Serialize a single BugReport instance to a binary Protocol Buffer message.

    Args:
        bug_report: Django BugReport model instance

    Returns:
        Binary serialized data
    """
    proto = django_to_proto(bug_report)
    return proto.SerializeToString()


def deserialize_bug_report(binary_data: bytes) -> BugReport:
    """
    Deserialize binary Protocol Buffer data to a BugReport instance.

    Args:
        binary_data: Binary serialized data

    Returns:
        Django BugReport model instance
    """
    proto = BugReportProto()
    proto.ParseFromString(binary_data)
    return proto_to_django(proto)
