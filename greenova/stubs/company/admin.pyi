from _typeshed import Incomplete
from django.contrib import admin
from django.db.models import Model
from django.http import HttpRequest
from typing import Any

logger: Incomplete

class BaseModelAdmin(admin.ModelAdmin):
    def dispatch(self, request: HttpRequest, object_id: Any, from_field: str | None = None) -> Model | None: ...

class CompanyAdmin(BaseModelAdmin):
    list_display: Incomplete
    list_filter: Incomplete
    search_fields: Incomplete
