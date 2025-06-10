from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObligationProto(_message.Message):
    __slots__ = ["obligation_number", "project_id", "primary_environmental_mechanism_id", "procedure", "environmental_aspect", "custom_environmental_aspect", "obligation", "accountability", "responsible_user_ids", "project_phase", "action_due_date", "close_out_date", "status", "supporting_information", "general_comments", "evidence_notes", "recurring_obligation", "recurring_frequency", "recurring_status", "recurring_forecasted_date", "inspection", "inspection_frequency", "site_or_desktop", "new_control_action_required", "obligation_type", "gap_analysis", "notes_for_gap_analysis", "created_at", "updated_at"]
    OBLIGATION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PRIMARY_ENVIRONMENTAL_MECHANISM_ID_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENTAL_ASPECT_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_ENVIRONMENTAL_ASPECT_FIELD_NUMBER: _ClassVar[int]
    OBLIGATION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTABILITY_FIELD_NUMBER: _ClassVar[int]
    RESPONSIBLE_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    PROJECT_PHASE_FIELD_NUMBER: _ClassVar[int]
    ACTION_DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    CLOSE_OUT_DATE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    SUPPORTING_INFORMATION_FIELD_NUMBER: _ClassVar[int]
    GENERAL_COMMENTS_FIELD_NUMBER: _ClassVar[int]
    EVIDENCE_NOTES_FIELD_NUMBER: _ClassVar[int]
    RECURRING_OBLIGATION_FIELD_NUMBER: _ClassVar[int]
    RECURRING_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    RECURRING_STATUS_FIELD_NUMBER: _ClassVar[int]
    RECURRING_FORECASTED_DATE_FIELD_NUMBER: _ClassVar[int]
    INSPECTION_FIELD_NUMBER: _ClassVar[int]
    INSPECTION_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    SITE_OR_DESKTOP_FIELD_NUMBER: _ClassVar[int]
    NEW_CONTROL_ACTION_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    OBLIGATION_TYPE_FIELD_NUMBER: _ClassVar[int]
    GAP_ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    NOTES_FOR_GAP_ANALYSIS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    obligation_number: str
    project_id: str
    primary_environmental_mechanism_id: str
    procedure: str
    environmental_aspect: str
    custom_environmental_aspect: str
    obligation: str
    accountability: str
    responsible_user_ids: _containers.RepeatedScalarFieldContainer[str]
    project_phase: str
    action_due_date: str
    close_out_date: str
    status: str
    supporting_information: str
    general_comments: str
    evidence_notes: str
    recurring_obligation: bool
    recurring_frequency: str
    recurring_status: str
    recurring_forecasted_date: str
    inspection: bool
    inspection_frequency: str
    site_or_desktop: str
    new_control_action_required: bool
    obligation_type: str
    gap_analysis: bool
    notes_for_gap_analysis: str
    created_at: str
    updated_at: str
    def __init__(self, obligation_number: _Optional[str] = ..., project_id: _Optional[str] = ..., primary_environmental_mechanism_id: _Optional[str] = ..., procedure: _Optional[str] = ..., environmental_aspect: _Optional[str] = ..., custom_environmental_aspect: _Optional[str] = ..., obligation: _Optional[str] = ..., accountability: _Optional[str] = ..., responsible_user_ids: _Optional[_Iterable[str]] = ..., project_phase: _Optional[str] = ..., action_due_date: _Optional[str] = ..., close_out_date: _Optional[str] = ..., status: _Optional[str] = ..., supporting_information: _Optional[str] = ..., general_comments: _Optional[str] = ..., evidence_notes: _Optional[str] = ..., recurring_obligation: bool = ..., recurring_frequency: _Optional[str] = ..., recurring_status: _Optional[str] = ..., recurring_forecasted_date: _Optional[str] = ..., inspection: bool = ..., inspection_frequency: _Optional[str] = ..., site_or_desktop: _Optional[str] = ..., new_control_action_required: bool = ..., obligation_type: _Optional[str] = ..., gap_analysis: bool = ..., notes_for_gap_analysis: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class ObligationCollection(_message.Message):
    __slots__ = ["obligations"]
    OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    obligations: _containers.RepeatedCompositeFieldContainer[ObligationProto]
    def __init__(self, obligations: _Optional[_Iterable[_Union[ObligationProto, _Mapping]]] = ...) -> None: ...
