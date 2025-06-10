from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Obligation(_message.Message):
    __slots__ = ["id", "title", "description", "status", "due_date", "project_id", "requirements", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    REQUIREMENTS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    title: str
    description: str
    status: str
    due_date: str
    project_id: int
    requirements: _containers.RepeatedCompositeFieldContainer[Requirement]
    created_at: int
    updated_at: int
    def __init__(self, id: _Optional[int] = ..., title: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[str] = ..., due_date: _Optional[str] = ..., project_id: _Optional[int] = ..., requirements: _Optional[_Iterable[_Union[Requirement, _Mapping]]] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ...) -> None: ...

class Requirement(_message.Message):
    __slots__ = ["id", "name", "description", "compliance_status", "tags"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COMPLIANCE_STATUS_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    compliance_status: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., compliance_status: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class Project(_message.Message):
    __slots__ = ["id", "name", "description", "location", "obligations", "metadata", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LOCATION_FIELD_NUMBER: _ClassVar[int]
    OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: int
    name: str
    description: str
    location: str
    obligations: _containers.RepeatedCompositeFieldContainer[Obligation]
    metadata: ProjectMetadata
    created_at: int
    updated_at: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., location: _Optional[str] = ..., obligations: _Optional[_Iterable[_Union[Obligation, _Mapping]]] = ..., metadata: _Optional[_Union[ProjectMetadata, _Mapping]] = ..., created_at: _Optional[int] = ..., updated_at: _Optional[int] = ...) -> None: ...

class ProjectMetadata(_message.Message):
    __slots__ = ["environmental_zone", "compliance_frameworks", "project_manager", "contact_email"]
    ENVIRONMENTAL_ZONE_FIELD_NUMBER: _ClassVar[int]
    COMPLIANCE_FRAMEWORKS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_MANAGER_FIELD_NUMBER: _ClassVar[int]
    CONTACT_EMAIL_FIELD_NUMBER: _ClassVar[int]
    environmental_zone: str
    compliance_frameworks: _containers.RepeatedScalarFieldContainer[str]
    project_manager: str
    contact_email: str
    def __init__(self, environmental_zone: _Optional[str] = ..., compliance_frameworks: _Optional[_Iterable[str]] = ..., project_manager: _Optional[str] = ..., contact_email: _Optional[str] = ...) -> None: ...

class DashboardData(_message.Message):
    __slots__ = ["project_summary", "obligation_summaries", "compliance_metrics", "last_updated"]
    PROJECT_SUMMARY_FIELD_NUMBER: _ClassVar[int]
    OBLIGATION_SUMMARIES_FIELD_NUMBER: _ClassVar[int]
    COMPLIANCE_METRICS_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    project_summary: ProjectSummary
    obligation_summaries: _containers.RepeatedCompositeFieldContainer[ObligationSummary]
    compliance_metrics: ComplianceMetrics
    last_updated: int
    def __init__(self, project_summary: _Optional[_Union[ProjectSummary, _Mapping]] = ..., obligation_summaries: _Optional[_Iterable[_Union[ObligationSummary, _Mapping]]] = ..., compliance_metrics: _Optional[_Union[ComplianceMetrics, _Mapping]] = ..., last_updated: _Optional[int] = ...) -> None: ...

class ProjectSummary(_message.Message):
    __slots__ = ["total_projects", "active_projects", "completed_projects", "recent_projects"]
    TOTAL_PROJECTS_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_PROJECTS_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_PROJECTS_FIELD_NUMBER: _ClassVar[int]
    RECENT_PROJECTS_FIELD_NUMBER: _ClassVar[int]
    total_projects: int
    active_projects: int
    completed_projects: int
    recent_projects: _containers.RepeatedCompositeFieldContainer[Project]
    def __init__(self, total_projects: _Optional[int] = ..., active_projects: _Optional[int] = ..., completed_projects: _Optional[int] = ..., recent_projects: _Optional[_Iterable[_Union[Project, _Mapping]]] = ...) -> None: ...

class ObligationSummary(_message.Message):
    __slots__ = ["status", "count", "upcoming_obligations"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    UPCOMING_OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    status: str
    count: int
    upcoming_obligations: _containers.RepeatedCompositeFieldContainer[Obligation]
    def __init__(self, status: _Optional[str] = ..., count: _Optional[int] = ..., upcoming_obligations: _Optional[_Iterable[_Union[Obligation, _Mapping]]] = ...) -> None: ...

class ComplianceMetrics(_message.Message):
    __slots__ = ["overall_compliance_rate", "overdue_obligations", "due_this_week", "due_this_month", "compliance_by_framework"]
    OVERALL_COMPLIANCE_RATE_FIELD_NUMBER: _ClassVar[int]
    OVERDUE_OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    DUE_THIS_WEEK_FIELD_NUMBER: _ClassVar[int]
    DUE_THIS_MONTH_FIELD_NUMBER: _ClassVar[int]
    COMPLIANCE_BY_FRAMEWORK_FIELD_NUMBER: _ClassVar[int]
    overall_compliance_rate: float
    overdue_obligations: int
    due_this_week: int
    due_this_month: int
    compliance_by_framework: _containers.RepeatedCompositeFieldContainer[ComplianceByFramework]
    def __init__(self, overall_compliance_rate: _Optional[float] = ..., overdue_obligations: _Optional[int] = ..., due_this_week: _Optional[int] = ..., due_this_month: _Optional[int] = ..., compliance_by_framework: _Optional[_Iterable[_Union[ComplianceByFramework, _Mapping]]] = ...) -> None: ...

class ComplianceByFramework(_message.Message):
    __slots__ = ["framework_name", "compliance_rate", "total_obligations", "compliant_obligations"]
    FRAMEWORK_NAME_FIELD_NUMBER: _ClassVar[int]
    COMPLIANCE_RATE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    COMPLIANT_OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    framework_name: str
    compliance_rate: float
    total_obligations: int
    compliant_obligations: int
    def __init__(self, framework_name: _Optional[str] = ..., compliance_rate: _Optional[float] = ..., total_obligations: _Optional[int] = ..., compliant_obligations: _Optional[int] = ...) -> None: ...
