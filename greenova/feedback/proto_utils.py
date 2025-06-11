# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protocol buffer utilities for the feedback app.

This module provides serialization and deserialization functions for
converting between Django models and Protocol Buffer messages in the
feedback application.
"""

import logging
import sys
from typing import Any

from django.contrib.auth import get_user_model

from .models import BugReport

User = get_user_model()
logger = logging.getLogger(__name__)

# Import generated protobuf modules with improved error handling
try:
<<<<<<< HEAD
    from .proto import feedback_pb2
||||||| parent of 37e6b25 (Squashed commit of the following:)
    from .proto import feedback_pb2
=======
    from . import feedback_pb2
>>>>>>> 37e6b25 (Squashed commit of the following:)

    logger.info("Successfully imported feedback_pb2 from proto subdirectory")
except ImportError:
    logger.exception(
        "feedback_pb2 module not found. Ensure to compile the protobuf files."
    )

    # Create a minimal stub for the module to allow Django to continue loading
    from types import ModuleType

    feedback_pb2: ModuleType = ModuleType("feedback_pb2")
    sys.modules["feedback.proto.feedback_pb2"] = feedback_pb2

    # Define minimal classes needed for type hinting
    class BugReportProto:
        """Stub class for BugReport protocol buffer message."""

        # pylint: disable=too-many-instance-attributes
<<<<<<< HEAD
        def __init__(self):
            """Initialize BugReportProto stub with default values."""
||||||| parent of 37e6b25 (Squashed commit of the following:)
        def __init__(self):
=======
        def __init__(self) -> None:
>>>>>>> 37e6b25 (Squashed commit of the following:)
            # Core fields that must be instance attributes
            self.id = 0
            self.title = ""
            self.description = ""
            # Environment fields
            self.application_version = ""
            self.operating_system = ""
            self.browser = ""
            self.device_type = ""
            # Problem details
            self.steps_to_reproduce = ""
            self.expected_behavior = ""
            self.actual_behavior = ""
            # Additional properties
            self.environment = ""
            self.error_messages = ""
            self.trace_report = ""
            self.frequency = 0
            self.impact_severity = ""
            self.user_impact = ""
            self.workarounds = ""
            self.additional_comments = ""
            self.github_issue_url = ""
            self.severity = ""
            self.status = ""
            self.admin_comment = ""
            self.reports = []

        # Define enum-like classes for consistency
        class Frequency:
            """Enum-like class for bug report frequency values."""

            FREQUENCY_UNKNOWN_UNSPECIFIED = 0
            FREQUENCY_ALWAYS = 1
            FREQUENCY_FREQUENTLY = 2
            FREQUENCY_OCCASIONALLY = 3
            FREQUENCY_RARELY = 4

        class Severity:
            """Enum-like class for bug report severity values."""

            SEVERITY_UNDEFINED_UNSPECIFIED = 0
            SEVERITY_LOW = 1
            SEVERITY_MEDIUM = 2
            SEVERITY_HIGH = 3
            SEVERITY_CRITICAL = 4

        class Status:
            """Enum-like class for bug report status values."""

            STATUS_UNSPECIFIED = 0
            STATUS_OPEN = 1
            STATUS_IN_PROGRESS = 2
            STATUS_RESOLVED = 3
            STATUS_CLOSED = 4
            STATUS_REJECTED = 5

<<<<<<< HEAD
        def serialize_to_string(self) -> bytes:
            """Serialize the BugReportProto to bytes (stub)."""
||||||| parent of 37e6b25 (Squashed commit of the following:)
        def SerializeToString(self) -> bytes:
            return b''
=======
        def SerializeToString(self) -> bytes:
>>>>>>> 37e6b25 (Squashed commit of the following:)
            return b""

        def parse_from_string(self, data: bytes) -> None:
            """Parse bytes into the BugReportProto (stub)."""
            # No-op for stub

    class BugReportCollection:
<<<<<<< HEAD
        """Stub class for a collection of BugReport protocol buffer messages."""

        def __init__(self):
            """Initialize BugReportCollection stub with empty report list."""
||||||| parent of 37e6b25 (Squashed commit of the following:)
        def __init__(self):
=======
        def __init__(self) -> None:
>>>>>>> 37e6b25 (Squashed commit of the following:)
            self.reports = []

<<<<<<< HEAD
        def serialize_to_string(self) -> bytes:
            """Serialize the BugReportCollection to bytes (stub)."""
||||||| parent of 37e6b25 (Squashed commit of the following:)
        def SerializeToString(self) -> bytes:
            return b''
=======
        def SerializeToString(self) -> bytes:
>>>>>>> 37e6b25 (Squashed commit of the following:)
            return b""

        def parse_from_string(self, data: bytes) -> None:
            """Parse bytes into the BugReportCollection (stub)."""
            # No-op for stub

        def append(self, item: Any) -> None:
            """Append a BugReportProto to the collection (stub)."""
            self.reports.append(item)

    # Add the classes to the module
    feedback_pb2.BugReportProto = BugReportProto
    feedback_pb2.BugReportCollection = BugReportCollection


def serialize_bug_report(bug_report: BugReport) -> bytes | None:
<<<<<<< HEAD
    """
    Serialize a BugReport instance to a Protocol Buffer message.
||||||| parent of 37e6b25 (Squashed commit of the following:)
def serialize_bug_report(bug_report: BugReport) -> Optional[bytes]:
    """
    Serialize a BugReport instance to a Protocol Buffer message.
=======
    """Serialize a BugReport instance to a Protocol Buffer message.
>>>>>>> 37e6b25 (Squashed commit of the following:)

    Args:
        bug_report: The BugReport instance to serialize

    Returns:
        Serialized protocol buffer data as bytes, or None if serialization failed

    """
    try:
        # Create a new BugReportProto message
        proto = feedback_pb2.BugReportProto()

        # Set basic fields
        proto.id = bug_report.id or 0
        proto.title = bug_report.title
        proto.description = bug_report.description

        # Set environment fields if available
        if hasattr(bug_report, "application_version"):
            proto.application_version = bug_report.application_version
        if hasattr(bug_report, "operating_system"):
            proto.operating_system = bug_report.operating_system
        if hasattr(bug_report, "browser"):
            proto.browser = bug_report.browser or ""
        if hasattr(bug_report, "device_type"):
            proto.device_type = bug_report.device_type

        # Set problem detail fields if available
        if hasattr(bug_report, "steps_to_reproduce"):
            proto.steps_to_reproduce = bug_report.steps_to_reproduce
        if hasattr(bug_report, "expected_behavior"):
            proto.expected_behavior = bug_report.expected_behavior
        if hasattr(bug_report, "actual_behavior"):
            proto.actual_behavior = bug_report.actual_behavior

        # Serialize to bytes
        return proto.serialize_to_string()
    except (AttributeError, TypeError) as e:
<<<<<<< HEAD
        logger.error(
||||||| parent of 37e6b25 (Squashed commit of the following:)
        logger.error(
            "Failed to serialize bug report due to attribute or type error: %s",
            str(e)
=======
        logger.exception(
>>>>>>> 37e6b25 (Squashed commit of the following:)
            "Failed to serialize bug report due to attribute or type error: %s", str(e)
        )
        return None
    except ValueError as e:
        logger.exception(
            "Failed to serialize bug report due to invalid value: %s", str(e)
        )
        return None


def deserialize_bug_report(data: bytes) -> BugReport | None:
<<<<<<< HEAD
    """
    Deserialize Protocol Buffer data to a BugReport instance.
||||||| parent of 37e6b25 (Squashed commit of the following:)
def deserialize_bug_report(data: bytes) -> Optional[BugReport]:
    """
    Deserialize Protocol Buffer data to a BugReport instance.
=======
    """Deserialize Protocol Buffer data to a BugReport instance.
>>>>>>> 37e6b25 (Squashed commit of the following:)

    Args:
        data: Serialized protocol buffer data

    Returns:
        BugReport instance or None if deserialization failed

    """
    try:
        # Parse the binary data into a BugReportProto
        proto = feedback_pb2.BugReportProto()
        proto.parse_from_string(data)

        # Create a BugReport instance
        bug_report = BugReport()

        # Set basic fields
        bug_report.title = proto.title
        bug_report.description = proto.description

        # Set environment fields
        if hasattr(proto, "application_version"):
            bug_report.application_version = proto.application_version
        if hasattr(proto, "operating_system"):
            bug_report.operating_system = proto.operating_system
        if hasattr(proto, "browser"):
            bug_report.browser = proto.browser
        if hasattr(proto, "device_type"):
            bug_report.device_type = proto.device_type

        # Set problem detail fields
        if hasattr(proto, "steps_to_reproduce"):
            bug_report.steps_to_reproduce = proto.steps_to_reproduce
        if hasattr(proto, "expected_behavior"):
            bug_report.expected_behavior = proto.expected_behavior
        if hasattr(proto, "actual_behavior"):
            bug_report.actual_behavior = proto.actual_behavior

        return bug_report
    except (AttributeError, TypeError) as e:
        logger.exception(
            "Failed to deserialize bug report due to attribute or type error: %s",
            str(e),
        )
        return None
    except ValueError as e:
<<<<<<< HEAD
        logger.error(
||||||| parent of 37e6b25 (Squashed commit of the following:)
        logger.error(
            "Failed to deserialize bug report due to invalid value: %s",
            str(e)
=======
        logger.exception(
>>>>>>> 37e6b25 (Squashed commit of the following:)
            "Failed to deserialize bug report due to invalid value: %s", str(e)
        )
        return None
    except (OSError, SystemError, OverflowError) as e:
        logger.exception("Failed to deserialize bug report: %s", str(e))
        return None


def serialize_bug_reports(bug_reports: list[BugReport]) -> bytes | None:
<<<<<<< HEAD
    """
    Serialize a list of BugReport instances to Protocol Buffer collection.
||||||| parent of 37e6b25 (Squashed commit of the following:)
def serialize_bug_reports(bug_reports: List[BugReport]) -> Optional[bytes]:
    """
    Serialize a list of BugReport instances to Protocol Buffer collection.
=======
    """Serialize a list of BugReport instances to Protocol Buffer collection.
>>>>>>> 37e6b25 (Squashed commit of the following:)

    Args:
        bug_reports: List of BugReport instances to serialize

    Returns:
        Serialized protocol buffer collection as bytes, or None if serialization failed

    """
    try:
        # Create a new BugReportCollection message
        collection = feedback_pb2.BugReportCollection()

        # Add each bug report to the collection
        for bug_report in bug_reports:
            report_proto_data = serialize_bug_report(bug_report)
            if report_proto_data:
                report_proto = feedback_pb2.BugReportProto()
                report_proto.parse_from_string(report_proto_data)
                collection.append(report_proto)

        # Serialize the collection to bytes
        return collection.serialize_to_string()
    except (AttributeError, TypeError) as e:
        logger.exception(
            "Failed to serialize bug report collection due to attribute "
            "or type error: %s",
            str(e),
        )
        return None
    except ValueError as e:
<<<<<<< HEAD
        logger.error(
||||||| parent of 37e6b25 (Squashed commit of the following:)
        logger.error(
            "Failed to serialize bug report collection due to invalid value: %s",
            str(e)
=======
        logger.exception(
>>>>>>> 37e6b25 (Squashed commit of the following:)
            "Failed to serialize bug report collection due to invalid value: %s", str(e)
        )
        return None
    except (OSError, SystemError) as e:
        logger.exception("Failed to serialize bug report collection: %s", str(e))
        return None


def deserialize_bug_reports(data: bytes) -> list[BugReport]:
<<<<<<< HEAD
    """
    Deserialize Protocol Buffer collection data to a list of BugReport instances.
||||||| parent of 37e6b25 (Squashed commit of the following:)
def deserialize_bug_reports(data: bytes) -> List[BugReport]:
    """
    Deserialize Protocol Buffer collection data to a list of BugReport instances.
=======
    """Deserialize Protocol Buffer collection data to a list of BugReport instances.
>>>>>>> 37e6b25 (Squashed commit of the following:)

    Args:
        data: Serialized protocol buffer collection

    Returns:
        List of BugReport instances

    """
    try:
        # Parse the binary data into a BugReportCollection
        collection = feedback_pb2.BugReportCollection()
        collection.parse_from_string(data)

        # Convert each protocol buffer message to a BugReport
        bug_reports = []
        for report_proto in collection.reports:
            # Serialize and deserialize each report
            report_data = report_proto.serialize_to_string()
            bug_report = deserialize_bug_report(report_data)
            if bug_report:
                bug_reports.append(bug_report)

        return bug_reports
    except (AttributeError, TypeError) as e:
        logger.exception(
            "Failed to deserialize bug report collection due to attribute "
            "or type error: %s",
            str(e),
        )
        return []
    except ValueError as e:
        logger.exception(
            "Failed to deserialize bug report collection due to invalid value: %s",
            str(e),
        )
        return []
    except (OSError, SystemError) as e:
        logger.exception(
            "Failed to deserialize bug report collection due to system error: %s",
            str(e),
        )
        return []
