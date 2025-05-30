"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Type definitions for the Greenova project."""

from django_htmx.middleware import HtmxDetails
from django.http import HttpRequest as HttpRequestBase
from django.db.models import QuerySet as DjangoQuerySet
from django.db.models import Model
from collections import UserDict
from typing import TypeVar


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
