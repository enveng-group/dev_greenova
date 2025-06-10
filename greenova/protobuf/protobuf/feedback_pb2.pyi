from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BugReportProto(_message.Message):
    __slots__ = ["id", "title", "description", "application_version", "operating_system", "browser", "device_type", "steps_to_reproduce", "expected_behavior", "actual_behavior", "error_messages", "trace_report", "frequency", "impact_severity", "admin_severity", "user_impact", "workarounds", "additional_comments", "user_id", "username", "created_at", "updated_at", "github_issue_url", "status", "admin_comment"]
    class Frequency(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        FREQUENCY_UNKNOWN_UNSPECIFIED: _ClassVar[BugReportProto.Frequency]
        FREQUENCY_ALWAYS: _ClassVar[BugReportProto.Frequency]
        FREQUENCY_FREQUENTLY: _ClassVar[BugReportProto.Frequency]
        FREQUENCY_OCCASIONALLY: _ClassVar[BugReportProto.Frequency]
        FREQUENCY_RARELY: _ClassVar[BugReportProto.Frequency]
    FREQUENCY_UNKNOWN_UNSPECIFIED: BugReportProto.Frequency
    FREQUENCY_ALWAYS: BugReportProto.Frequency
    FREQUENCY_FREQUENTLY: BugReportProto.Frequency
    FREQUENCY_OCCASIONALLY: BugReportProto.Frequency
    FREQUENCY_RARELY: BugReportProto.Frequency
    class Severity(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        SEVERITY_UNDEFINED_UNSPECIFIED: _ClassVar[BugReportProto.Severity]
        SEVERITY_LOW: _ClassVar[BugReportProto.Severity]
        SEVERITY_MEDIUM: _ClassVar[BugReportProto.Severity]
        SEVERITY_HIGH: _ClassVar[BugReportProto.Severity]
        SEVERITY_CRITICAL: _ClassVar[BugReportProto.Severity]
    SEVERITY_UNDEFINED_UNSPECIFIED: BugReportProto.Severity
    SEVERITY_LOW: BugReportProto.Severity
    SEVERITY_MEDIUM: BugReportProto.Severity
    SEVERITY_HIGH: BugReportProto.Severity
    SEVERITY_CRITICAL: BugReportProto.Severity
    class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
        STATUS_UNSPECIFIED: _ClassVar[BugReportProto.Status]
        STATUS_OPEN: _ClassVar[BugReportProto.Status]
        STATUS_IN_PROGRESS: _ClassVar[BugReportProto.Status]
        STATUS_RESOLVED: _ClassVar[BugReportProto.Status]
        STATUS_CLOSED: _ClassVar[BugReportProto.Status]
        STATUS_REJECTED: _ClassVar[BugReportProto.Status]
    STATUS_UNSPECIFIED: BugReportProto.Status
    STATUS_OPEN: BugReportProto.Status
    STATUS_IN_PROGRESS: BugReportProto.Status
    STATUS_RESOLVED: BugReportProto.Status
    STATUS_CLOSED: BugReportProto.Status
    STATUS_REJECTED: BugReportProto.Status
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_VERSION_FIELD_NUMBER: _ClassVar[int]
    OPERATING_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    BROWSER_FIELD_NUMBER: _ClassVar[int]
    DEVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    STEPS_TO_REPRODUCE_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_BEHAVIOR_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TRACE_REPORT_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    IMPACT_SEVERITY_FIELD_NUMBER: _ClassVar[int]
    ADMIN_SEVERITY_FIELD_NUMBER: _ClassVar[int]
    USER_IMPACT_FIELD_NUMBER: _ClassVar[int]
    WORKAROUNDS_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_COMMENTS_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    GITHUB_ISSUE_URL_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ADMIN_COMMENT_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    description: str
    application_version: str
    operating_system: str
    browser: str
    device_type: str
    steps_to_reproduce: str
    expected_behavior: str
    actual_behavior: str
    error_messages: str
    trace_report: str
    frequency: BugReportProto.Frequency
    impact_severity: BugReportProto.Severity
    admin_severity: BugReportProto.Severity
    user_impact: str
    workarounds: str
    additional_comments: str
    user_id: int
    username: str
    created_at: int
    updated_at: int
    github_issue_url: str
    status: BugReportProto.Status
    admin_comment: str
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., application_version: _Optional[str] = ..., operating_system: _Optional[str] = ..., browser: _Optional[str] = ..., device_type: _Optional[str] = ..., steps_to_reproduce: _Optional[str] = ..., expected_behavior: _Optional[str] = ..., actual_behavior: _Optional[str] = ..., error_messages: _Optional[str] = ..., trace_report: _Optional[str] = ..., frequency: _Optional[_Union[BugReportProto.Frequency, str]] = ..., impact_severity: _Optional[_Union[BugReportProto.Severity, str]] = ..., admin_severity: _Optional[_Union[BugReportProto.Severity, str]] = ..., user_impact: _Optional[str] = ..., workarounds: _Optional[str] = ..., additional_comments: _Optional[str] = ..., user_id: _Optional[int] = ..., username: _Optional[str] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ..., github_issue_url: _Optional[str] = ..., status: _Optional[_Union[BugReportProto.Status, str]] = ..., admin_comment: _Optional[str] = ...) -> None: ...

class BugReportCollection(_message.Message):
    __slots__ = ["reports"]
    REPORTS_FIELD_NUMBER: _ClassVar[int]
    reports: _containers.RepeatedCompositeFieldContainer[BugReportProto]
    def __init__(self, reports: _Optional[_Iterable[_Union[BugReportProto, _Mapping]]] = ...) -> None: ...
