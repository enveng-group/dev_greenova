from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObligationStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    STATUS_UNKNOWN: _ClassVar[ObligationStatus]
    STATUS_NOT_STARTED: _ClassVar[ObligationStatus]
    STATUS_IN_PROGRESS: _ClassVar[ObligationStatus]
    STATUS_COMPLETED: _ClassVar[ObligationStatus]
    STATUS_OVERDUE: _ClassVar[ObligationStatus]
STATUS_UNKNOWN: ObligationStatus
STATUS_NOT_STARTED: ObligationStatus
STATUS_IN_PROGRESS: ObligationStatus
STATUS_COMPLETED: ObligationStatus
STATUS_OVERDUE: ObligationStatus

class ObligationInsight(_message.Message):
    __slots__ = ["obligation_number", "due_date", "close_out_date"]
    OBLIGATION_NUMBER_FIELD_NUMBER: _ClassVar[int]
    DUE_DATE_FIELD_NUMBER: _ClassVar[int]
    CLOSE_OUT_DATE_FIELD_NUMBER: _ClassVar[int]
    obligation_number: str
    due_date: str
    close_out_date: str
    def __init__(self, obligation_number: _Optional[str] = ..., due_date: _Optional[str] = ..., close_out_date: _Optional[str] = ...) -> None: ...

class ObligationInsightResponse(_message.Message):
    __slots__ = ["mechanism_id", "status", "status_key", "count", "total_count", "obligations", "error"]
    MECHANISM_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_KEY_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    TOTAL_COUNT_FIELD_NUMBER: _ClassVar[int]
    OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    mechanism_id: int
    status: str
    status_key: str
    count: int
    total_count: int
    obligations: _containers.RepeatedCompositeFieldContainer[ObligationInsight]
    error: str
    def __init__(self, mechanism_id: _Optional[int] = ..., status: _Optional[str] = ..., status_key: _Optional[str] = ..., count: _Optional[int] = ..., total_count: _Optional[int] = ..., obligations: _Optional[_Iterable[_Union[ObligationInsight, _Mapping]]] = ..., error: _Optional[str] = ...) -> None: ...

class ChartSegment(_message.Message):
    __slots__ = ["label", "value", "color"]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    label: str
    value: int
    color: str
    def __init__(self, label: _Optional[str] = ..., value: _Optional[int] = ..., color: _Optional[str] = ...) -> None: ...

class ChartData(_message.Message):
    __slots__ = ["segments", "mechanism_id", "mechanism_name"]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    MECHANISM_ID_FIELD_NUMBER: _ClassVar[int]
    MECHANISM_NAME_FIELD_NUMBER: _ClassVar[int]
    segments: _containers.RepeatedCompositeFieldContainer[ChartSegment]
    mechanism_id: int
    mechanism_name: str
    def __init__(self, segments: _Optional[_Iterable[_Union[ChartSegment, _Mapping]]] = ..., mechanism_id: _Optional[int] = ..., mechanism_name: _Optional[str] = ...) -> None: ...

class ChartResponse(_message.Message):
    __slots__ = ["charts", "error"]
    CHARTS_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    charts: _containers.RepeatedCompositeFieldContainer[ChartData]
    error: str
    def __init__(self, charts: _Optional[_Iterable[_Union[ChartData, _Mapping]]] = ..., error: _Optional[str] = ...) -> None: ...
