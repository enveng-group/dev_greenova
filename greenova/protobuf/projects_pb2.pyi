from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectProto(_message.Message):
    __slots__ = ["id", "name", "description", "member_user_ids", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    MEMBER_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    description: str
    member_user_ids: _containers.RepeatedScalarFieldContainer[str]
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., member_user_ids: _Optional[_Iterable[str]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class ProjectMembershipProto(_message.Message):
    __slots__ = ["id", "project_id", "user_id", "role", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    user_id: str
    role: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., user_id: _Optional[str] = ..., role: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class ProjectObligationProto(_message.Message):
    __slots__ = ["id", "project_id", "obligation_id", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_ID_FIELD_NUMBER: _ClassVar[int]
    OBLIGATION_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    project_id: str
    obligation_id: str
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., project_id: _Optional[str] = ..., obligation_id: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class ProjectCollection(_message.Message):
    __slots__ = ["projects"]
    PROJECTS_FIELD_NUMBER: _ClassVar[int]
    projects: _containers.RepeatedCompositeFieldContainer[ProjectProto]
    def __init__(self, projects: _Optional[_Iterable[_Union[ProjectProto, _Mapping]]] = ...) -> None: ...

class ProjectMembershipCollection(_message.Message):
    __slots__ = ["memberships"]
    MEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    memberships: _containers.RepeatedCompositeFieldContainer[ProjectMembershipProto]
    def __init__(self, memberships: _Optional[_Iterable[_Union[ProjectMembershipProto, _Mapping]]] = ...) -> None: ...

class ProjectObligationCollection(_message.Message):
    __slots__ = ["project_obligations"]
    PROJECT_OBLIGATIONS_FIELD_NUMBER: _ClassVar[int]
    project_obligations: _containers.RepeatedCompositeFieldContainer[ProjectObligationProto]
    def __init__(self, project_obligations: _Optional[_Iterable[_Union[ProjectObligationProto, _Mapping]]] = ...) -> None: ...
