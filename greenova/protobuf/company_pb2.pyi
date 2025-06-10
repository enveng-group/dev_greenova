from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CompanyProto(_message.Message):
    __slots__ = ["id", "name", "logo_url", "description", "website", "address", "phone", "email", "company_type", "size", "industry", "is_active", "member_user_ids", "created_at", "updated_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LOGO_URL_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PHONE_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    COMPANY_TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    INDUSTRY_FIELD_NUMBER: _ClassVar[int]
    IS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    MEMBER_USER_IDS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    logo_url: str
    description: str
    website: str
    address: str
    phone: str
    email: str
    company_type: str
    size: str
    industry: str
    is_active: bool
    member_user_ids: _containers.RepeatedScalarFieldContainer[str]
    created_at: str
    updated_at: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., logo_url: _Optional[str] = ..., description: _Optional[str] = ..., website: _Optional[str] = ..., address: _Optional[str] = ..., phone: _Optional[str] = ..., email: _Optional[str] = ..., company_type: _Optional[str] = ..., size: _Optional[str] = ..., industry: _Optional[str] = ..., is_active: bool = ..., member_user_ids: _Optional[_Iterable[str]] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class CompanyMembershipProto(_message.Message):
    __slots__ = ["id", "company_id", "user_id", "role", "department", "position", "date_joined", "is_primary"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    DEPARTMENT_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    DATE_JOINED_FIELD_NUMBER: _ClassVar[int]
    IS_PRIMARY_FIELD_NUMBER: _ClassVar[int]
    id: str
    company_id: str
    user_id: str
    role: str
    department: str
    position: str
    date_joined: str
    is_primary: bool
    def __init__(self, id: _Optional[str] = ..., company_id: _Optional[str] = ..., user_id: _Optional[str] = ..., role: _Optional[str] = ..., department: _Optional[str] = ..., position: _Optional[str] = ..., date_joined: _Optional[str] = ..., is_primary: bool = ...) -> None: ...

class CompanyDocumentProto(_message.Message):
    __slots__ = ["id", "company_id", "name", "description", "file_url", "document_type", "uploaded_by_user_id", "uploaded_at"]
    ID_FIELD_NUMBER: _ClassVar[int]
    COMPANY_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    FILE_URL_FIELD_NUMBER: _ClassVar[int]
    DOCUMENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    UPLOADED_BY_USER_ID_FIELD_NUMBER: _ClassVar[int]
    UPLOADED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    company_id: str
    name: str
    description: str
    file_url: str
    document_type: str
    uploaded_by_user_id: str
    uploaded_at: str
    def __init__(self, id: _Optional[str] = ..., company_id: _Optional[str] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., file_url: _Optional[str] = ..., document_type: _Optional[str] = ..., uploaded_by_user_id: _Optional[str] = ..., uploaded_at: _Optional[str] = ...) -> None: ...

class CompanyCollection(_message.Message):
    __slots__ = ["companies"]
    COMPANIES_FIELD_NUMBER: _ClassVar[int]
    companies: _containers.RepeatedCompositeFieldContainer[CompanyProto]
    def __init__(self, companies: _Optional[_Iterable[_Union[CompanyProto, _Mapping]]] = ...) -> None: ...

class CompanyMembershipCollection(_message.Message):
    __slots__ = ["memberships"]
    MEMBERSHIPS_FIELD_NUMBER: _ClassVar[int]
    memberships: _containers.RepeatedCompositeFieldContainer[CompanyMembershipProto]
    def __init__(self, memberships: _Optional[_Iterable[_Union[CompanyMembershipProto, _Mapping]]] = ...) -> None: ...

class CompanyDocumentCollection(_message.Message):
    __slots__ = ["documents"]
    DOCUMENTS_FIELD_NUMBER: _ClassVar[int]
    documents: _containers.RepeatedCompositeFieldContainer[CompanyDocumentProto]
    def __init__(self, documents: _Optional[_Iterable[_Union[CompanyDocumentProto, _Mapping]]] = ...) -> None: ...
