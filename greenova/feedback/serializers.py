# Copyright 2025 Enveng Group.
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Protobuf3-based serializers for the feedback app."""

from django.core.exceptions import ValidationError

from .models import BugReport
from .proto_utils import (
    deserialize_bug_report,
    deserialize_bug_reports,
    serialize_bug_report,
    serialize_bug_reports,
)


class BugReportProtoSerializer:
    """Serializer for BugReport using protobuf3 binary format.

    Accepts and returns protobuf3 binary data. Uses proto_utils for conversion.
    """

    def __init__(
        self,
        instance: BugReport | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instance = instance
        self.initial_data = data
        self.validated_data: BugReport | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        bug_report = deserialize_bug_report(self.initial_data)
        if bug_report is None:
            self.errors = "Invalid protobuf data."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = bug_report
        return True

    def save(self) -> BugReport:
        if self.validated_data is None:
            msg = "Call is_valid() before save()."
            raise ValidationError(msg)
        self.validated_data.save()
        self.instance = self.validated_data
        return self.instance

    def data(self) -> bytes | None:
        if self.instance is None:
            return None
        return serialize_bug_report(self.instance)


class BugReportCollectionProtoSerializer:
    """Serializer for a collection of BugReport instances using protobuf3."""

    def __init__(
        self,
        instances: list[BugReport] | None = None,
        data: bytes | None = None,
    ) -> None:
        self.instances = instances
        self.initial_data = data
        self.validated_data: list[BugReport] | None = None
        self.errors: str | None = None

    def is_valid(self, raise_exception: bool = False) -> bool:
        if self.initial_data is None:
            self.errors = "No data provided."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        bug_reports = deserialize_bug_reports(self.initial_data)
        if not bug_reports:
            self.errors = "Invalid protobuf data or empty collection."
            if raise_exception:
                raise ValidationError(self.errors)
            return False
        self.validated_data = bug_reports
        return True

    def data(self) -> bytes | None:
        if self.instances is None:
            return None
        return serialize_bug_reports(self.instances)
