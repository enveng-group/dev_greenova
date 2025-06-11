from .models import EnvironmentalMechanism
from _typeshed import Incomplete
from django.contrib import admin
from django.forms import ModelForm
from django.http import HttpRequest
from typing import Any

class EnvironmentalMechanismAdmin(admin.ModelAdmin):
    list_display: Incomplete
    list_filter: Incomplete
    search_fields: Incomplete
    readonly_fields: Incomplete
    ordering: Incomplete
    fields: Incomplete
    def get_queryset(self, request: HttpRequest) -> Any: ...
    @staticmethod
    def get_total_obligations(obj: EnvironmentalMechanism) -> int: ...
    def save_model(self, request: HttpRequest, obj: EnvironmentalMechanism, form: ModelForm, change: bool) -> None: ...
    @staticmethod
    def is_overdue(obj: EnvironmentalMechanism) -> bool: ...
