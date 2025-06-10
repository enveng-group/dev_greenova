from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NewsletterSignupRequest(_message.Message):
    __slots__ = ["email"]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    email: str
    def __init__(self, email: _Optional[str] = ...) -> None: ...

class NewsletterSignupResponse(_message.Message):
    __slots__ = ["success", "message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...

class Feature(_message.Message):
    __slots__ = ["title", "description"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ...) -> None: ...

class Stat(_message.Message):
    __slots__ = ["name", "value"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: int
    def __init__(self, name: _Optional[str] = ..., value: _Optional[int] = ...) -> None: ...

class Testimonial(_message.Message):
    __slots__ = ["name", "content"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    name: str
    content: str
    def __init__(self, name: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class LandingPageContent(_message.Message):
    __slots__ = ["hero_title", "hero_subtitle", "features", "stats", "benefits", "testimonials", "cta_title", "cta_subtitle"]
    HERO_TITLE_FIELD_NUMBER: _ClassVar[int]
    HERO_SUBTITLE_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    STATS_FIELD_NUMBER: _ClassVar[int]
    BENEFITS_FIELD_NUMBER: _ClassVar[int]
    TESTIMONIALS_FIELD_NUMBER: _ClassVar[int]
    CTA_TITLE_FIELD_NUMBER: _ClassVar[int]
    CTA_SUBTITLE_FIELD_NUMBER: _ClassVar[int]
    hero_title: str
    hero_subtitle: str
    features: _containers.RepeatedCompositeFieldContainer[Feature]
    stats: _containers.RepeatedCompositeFieldContainer[Stat]
    benefits: _containers.RepeatedScalarFieldContainer[str]
    testimonials: _containers.RepeatedCompositeFieldContainer[Testimonial]
    cta_title: str
    cta_subtitle: str
    def __init__(self, hero_title: _Optional[str] = ..., hero_subtitle: _Optional[str] = ..., features: _Optional[_Iterable[_Union[Feature, _Mapping]]] = ..., stats: _Optional[_Iterable[_Union[Stat, _Mapping]]] = ..., benefits: _Optional[_Iterable[str]] = ..., testimonials: _Optional[_Iterable[_Union[Testimonial, _Mapping]]] = ..., cta_title: _Optional[str] = ..., cta_subtitle: _Optional[str] = ...) -> None: ...
