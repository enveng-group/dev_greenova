# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the feedback app.

This module provides serialization and deserialization functions for
converting between Django models and Protocol Buffer messages in the
feedback application.
"""

import logging
import os
import sys

from django.contrib.auth import get_user_model

from .models import BugReport

User = get_user_model()
logger = logging.getLogger(__name__)

# Import generated protobuf modules with improved error handling
try:
    from greenova.protobuf import feedback_pb2

    logger.info("Successfully imported feedback_pb2 from proto subdirectory")
except ImportError:
    logger.exception(
        "feedback_pb2 module not found. Ensure to compile the protobuf files.",
    )
    feedback_pb2 = None

    # Check if the proto file exists
    current_dir = os.path.dirname(os.path.abspath(__file__))
    proto_file = os.path.join(current_dir, "proto", "feedback.proto")

    if os.path.exists(proto_file):
        logger.info(
            "feedback.proto exists but feedback_pb2.py not found. "
            "Run 'python manage.py compile_protos --app=feedback' to generate it.",
        )
    else:
        logger.exception("feedback.proto file not found in the proto directory.")

    # Create a minimal stub for the module to allow Django to continue loading
    from types import ModuleType

    feedback_pb2 = ModuleType("feedback_pb2")
    sys.modules["feedback.proto.feedback_pb2"] = feedback_pb2

    # Define minimal classes needed for type hinting
    class BugReportProto:
        class Frequency:
            FREQUENCY_UNKNOWN_UNSPECIFIED = 0
            FREQUENCY_ALWAYS = 1
            FREQUENCY_FREQUENTLY = 2
            FREQUENCY_OCCASIONALLY = 3
            FREQUENCY_RARELY = 4

        class Severity:
            SEVERITY_UNDEFINED_UNSPECIFIED = 0
            SEVERITY_LOW = 1
            SEVERITY_MEDIUM = 2
            SEVERITY_HIGH = 3
            SEVERITY_CRITICAL = 4

        class Status:
            STATUS_UNSPECIFIED = 0
            STATUS_OPEN = 1
            STATUS_IN_PROGRESS = 2
            STATUS_RESOLVED = 3
            STATUS_CLOSED = 4
            STATUS_REJECTED = 5

        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
            pass

    class BugReportCollection:
        reports = []

        def SerializeToString(self) -> bytes:
            return b""

        def ParseFromString(self, data) -> None:
            pass

    feedback_pb2.BugReportProto = BugReportProto
    feedback_pb2.BugReportCollection = BugReportCollection


def serialize_bug_report(bug_report: BugReport) -> bytes | None:
    """Serialize a BugReport instance to a Protocol Buffer message.

    Args:
        bug_report: The BugReport instance to serialize

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed

    """
    try:
        # Use the model's to_pb method for serialization
        proto = bug_report.to_pb()  # type: ignore[attr-defined]
        return proto.SerializeToString()
    except Exception as e:
        logger.exception(
            "Failed to serialize bug report to protobuf: %s",
            str(e),
        )
        return None


def deserialize_bug_report(data: bytes) -> BugReport | None:
    """Deserialize Protocol Buffer data to a BugReport instance.

    Args:
        data: Serialized protocol buffer data

    Returns:
        BugReport instance or None if deserialization failed

    """
    try:
        # Parse the binary data into a BugReportProto
        proto = feedback_pb2.BugReportProto()
        proto.ParseFromString(data)
        # Use the model's from_pb method for deserialization
        return BugReport().from_pb(proto)  # type: ignore[attr-defined]
    except Exception as e:
        logger.exception(
            "Failed to deserialize bug report from protobuf: %s",
            str(e),
        )
        return None


def serialize_bug_reports(bug_reports: list[BugReport]) -> bytes | None:
    """Serialize a list of BugReport instances to Protocol Buffer collection.

    Args:
        bug_reports: List of BugReport instances to serialize

    Returns:
        Serialized protocol buffer collection as bytes, or None if serialization failed

    """
    try:
        collection = feedback_pb2.BugReportCollection()
        for bug_report in bug_reports:
            proto = bug_report.to_pb()  # type: ignore[attr-defined]
            collection.reports.append(proto)
        return collection.SerializeToString()
    except Exception as e:
        logger.exception(
            "Failed to serialize bug report collection to protobuf: %s",
            str(e),
        )
        return None


def deserialize_bug_reports(data: bytes) -> list[BugReport]:
    """Deserialize Protocol Buffer collection data to a list of BugReport instances.

    Args:
        data: Serialized protocol buffer collection

    Returns:
        List of BugReport instances

    """
    try:
        collection = feedback_pb2.BugReportCollection()
        collection.ParseFromString(data)
        bug_reports = []
        for report_proto in collection.reports:
            bug_report = BugReport().from_pb(report_proto)  # type: ignore[attr-defined]
            if bug_report:
                bug_reports.append(bug_report)
        return bug_reports
    except Exception as e:
        logger.exception(
            "Failed to deserialize bug report collection from protobuf: %s",
            str(e),
        )
        return []
