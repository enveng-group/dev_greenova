"""Type definitions for the Greenova project."""
from collections import UserDict
from typing import TypeVar

from django.db.models import Model
from django.db.models import QuerySet as DjangoQuerySet
from django.http import HttpRequest as HttpRequestBase
from django_htmx.middleware import HtmxDetails

# Type variable for generic model operations
T = TypeVar("T", bound=Model)


class HttpRequest(HttpRequestBase):
    """Enhanced HttpRequest class with HTMX support.

    This type definition helps static type checkers understand that
    request.htmx is available when using django-htmx middleware.
    """

    htmx: HtmxDetails


# Generic QuerySet type that can be used in models
class QuerySet[T: Model](DjangoQuerySet):
    """Enhanced QuerySet type for better type checking."""


# Common type for status data responses
class StatusData(UserDict[str, int]):
    """Type for status data dictionaries with string keys and integer values."""


# Exception handler types
class DjangoError:
    """Base class for custom Django error types."""


class ModelOperationError(DjangoError, Exception):
    """Error during model operations."""


# Type for model field choices
ChoicesType = list[tuple[str, str]]
