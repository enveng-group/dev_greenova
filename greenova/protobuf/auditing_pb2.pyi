from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MitigationProto(_message.Message):
    __slots__ = ["id", "audit_entry_id", "description", "status", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    audit_entry_id: str
    description: str
    status: str
    created_at: str
    def __init__(self, id: _Optional[str] = ..., audit_entry_id: _Optional[str] = ..., description: _Optional[str] = ..., status: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...

class CorrectiveActionProto(_message.Message):
    __slots__ = ["id", "mitigation_id", "task", "status", "assigned_to_user_id", "created_at", "due_date"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MITIGATION_ID_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    ASSIGNED_TO_USER_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    mitigation_id: str
    task: str
    status: str
    assigned_to_user_id: str
    created_at: str
    due_date: str
    def __init__(self, id: _Optional[str] = ..., mitigation_id: _Optional[str] = ..., task: _Optional[str] = ..., status: _Optional[str] = ..., assigned_to_user_id: _Optional[str] = ..., created_at: _Optional[str] = ..., due_date: _Optional[str] = ...) -> None: ...

class AuditProto(_message.Message):
    __slots__ = ["id", "name", "created_at", "mechanism_ids"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    MECHANISM_IDS_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    created_at: str
    mechanism_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., created_at: _Optional[str] = ..., mechanism_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class AuditEntryProto(_message.Message):
    __slots__ = ["id", "audit_id", "obligation_id", "status", "finding"]
    ID_FIELD_NUMBER: _ClassVar[int]
    AUDIT_ID_FIELD_NUMBER: _ClassVar[int]
    OBLIGATION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    FINDING_FIELD_NUMBER: _ClassVar[int]
    id: str
    audit_id: str
    obligation_id: str
    status: str
    finding: str
    def __init__(self, id: _Optional[str] = ..., audit_id: _Optional[str] = ..., obligation_id: _Optional[str] = ..., status: _Optional[str] = ..., finding: _Optional[str] = ...) -> None: ...

class ComplianceCommentProto(_message.Message):
    __slots__ = ["id", "obligation_id", "text", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    OBLIGATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    obligation_id: str
    text: str
    created_at: str
    def __init__(self, id: _Optional[str] = ..., obligation_id: _Optional[str] = ..., text: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...

class NonConformanceCommentProto(_message.Message):
    __slots__ = ["id", "obligation_id", "text", "created_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    OBLIGATION_ID_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    obligation_id: str
    text: str
    created_at: str
    def __init__(self, id: _Optional[str] = ..., obligation_id: _Optional[str] = ..., text: _Optional[str] = ..., created_at: _Optional[str] = ...) -> None: ...

class MitigationCollection(_message.Message):
    __slots__ = ["mitigations"]
    MITIGATIONS_FIELD_NUMBER: _ClassVar[int]
    mitigations: _containers.RepeatedCompositeFieldContainer[MitigationProto]
    def __init__(self, mitigations: _Optional[_Iterable[_Union[MitigationProto, _Mapping]]] = ...) -> None: ...

class CorrectiveActionCollection(_message.Message):
    __slots__ = ["corrective_actions"]
    CORRECTIVE_ACTIONS_FIELD_NUMBER: _ClassVar[int]
    corrective_actions: _containers.RepeatedCompositeFieldContainer[CorrectiveActionProto]
    def __init__(self, corrective_actions: _Optional[_Iterable[_Union[CorrectiveActionProto, _Mapping]]] = ...) -> None: ...

class AuditCollection(_message.Message):
    __slots__ = ["audits"]
    AUDITS_FIELD_NUMBER: _ClassVar[int]
    audits: _containers.RepeatedCompositeFieldContainer[AuditProto]
    def __init__(self, audits: _Optional[_Iterable[_Union[AuditProto, _Mapping]]] = ...) -> None: ...

class AuditEntryCollection(_message.Message):
    __slots__ = ["audit_entries"]
    AUDIT_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    audit_entries: _containers.RepeatedCompositeFieldContainer[AuditEntryProto]
    def __init__(self, audit_entries: _Optional[_Iterable[_Union[AuditEntryProto, _Mapping]]] = ...) -> None: ...

class ComplianceCommentCollection(_message.Message):
    __slots__ = ["compliance_comments"]
    COMPLIANCE_COMMENTS_FIELD_NUMBER: _ClassVar[int]
    compliance_comments: _containers.RepeatedCompositeFieldContainer[ComplianceCommentProto]
    def __init__(self, compliance_comments: _Optional[_Iterable[_Union[ComplianceCommentProto, _Mapping]]] = ...) -> None: ...

class NonConformanceCommentCollection(_message.Message):
    __slots__ = ["non_conformance_comments"]
    NON_CONFORMANCE_COMMENTS_FIELD_NUMBER: _ClassVar[int]
    non_conformance_comments: _containers.RepeatedCompositeFieldContainer[NonConformanceCommentProto]
    def __init__(self, non_conformance_comments: _Optional[_Iterable[_Union[NonConformanceCommentProto, _Mapping]]] = ...) -> None: ...
