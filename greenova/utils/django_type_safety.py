from typing import TypeVar, Generic, Optional, Any
from django.contrib.admin import ModelAdmin, TabularInline, StackedInline
from django.db import models
from django.http import HttpRequest

# Type variable for model classes
T = TypeVar('T', bound=models.Model)

class TypedModelAdmin(ModelAdmin, Generic[T]):
    """Type-safe version of ModelAdmin."""
    pass

    def get_object(self, request: HttpRequest, object_id: str, from_field: None = None) -> Optional[T]:
        return super().get_object(request, object_id, from_field)

class TypedTabularInline(TabularInline):
    """Type-safe version of TabularInline."""
    model: type[models.Model]

    def get_queryset(self, request: HttpRequest) -> models.QuerySet[Any]:
        return super().get_queryset(request)

class TypedStackedInline(StackedInline):
    """Type-safe version of StackedInline."""
    model: type[models.Model]

    def get_queryset(self, request: HttpRequest) -> models.QuerySet[Any]:
        return super().get_queryset(request)
