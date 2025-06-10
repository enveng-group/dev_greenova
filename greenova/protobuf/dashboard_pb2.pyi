from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DashboardWidget(_message.Message):
    __slots__ = ["id", "name", "type", "config_json"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    type: str
    config_json: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., type: _Optional[str] = ..., config_json: _Optional[str] = ...) -> None: ...

class DashboardLayout(_message.Message):
    __slots__ = ["widgets", "layout_json"]
    WIDGETS_FIELD_NUMBER: _ClassVar[int]
    LAYOUT_JSON_FIELD_NUMBER: _ClassVar[int]
    widgets: _containers.RepeatedCompositeFieldContainer[DashboardWidget]
    layout_json: str
    def __init__(self, widgets: _Optional[_Iterable[_Union[DashboardWidget, _Mapping]]] = ..., layout_json: _Optional[str] = ...) -> None: ...

class DashboardPreferences(_message.Message):
    __slots__ = ["user_id", "selected_project", "selected_mechanism", "preferences_json"]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    SELECTED_PROJECT_FIELD_NUMBER: _ClassVar[int]
    SELECTED_MECHANISM_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_JSON_FIELD_NUMBER: _ClassVar[int]
    user_id: str
    selected_project: str
    selected_mechanism: str
    preferences_json: str
    def __init__(self, user_id: _Optional[str] = ..., selected_project: _Optional[str] = ..., selected_mechanism: _Optional[str] = ..., preferences_json: _Optional[str] = ...) -> None: ...

class DashboardAPIResponse(_message.Message):
    __slots__ = ["layout", "preferences", "last_updated"]
    LAYOUT_FIELD_NUMBER: _ClassVar[int]
    PREFERENCES_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATED_FIELD_NUMBER: _ClassVar[int]
    layout: DashboardLayout
    preferences: DashboardPreferences
    last_updated: int
    def __init__(self, layout: _Optional[_Union[DashboardLayout, _Mapping]] = ..., preferences: _Optional[_Union[DashboardPreferences, _Mapping]] = ..., last_updated: _Optional[int] = ...) -> None: ...
