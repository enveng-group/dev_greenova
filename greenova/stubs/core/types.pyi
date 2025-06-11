from django.db.models import Model, QuerySet as DjangoQuerySet
from django.http import HttpRequest as HttpRequestBase
from django_htmx.middleware import HtmxDetails as HtmxDetails
from typing import Generic, TypeVar

T = TypeVar('T', bound=Model)

class HttpRequest(HttpRequestBase):
    htmx: HtmxDetails

class QuerySet(DjangoQuerySet, Generic[T]): ...
class StatusData(dict[str, int]): ...
class DjangoError: ...
class ModelOperationError(DjangoError, Exception): ...
ChoicesType = list[tuple[str, str]]
