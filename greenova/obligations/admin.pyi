from typing import Any

from _typeshed import Incomplete
from beartype import beartype
from django import forms
from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest

from .models import ComplianceComment as ComplianceComment
from .models import NonConformanceComment as NonConformanceComment
from .models import Obligation as Obligation
from .models import ObligationEvidence as ObligationEvidence

logger: Incomplete

class ComplianceInline(admin.TabularInline):
    model = ComplianceComment
    extra: int

class NonConformanceInline(admin.TabularInline):
    model = NonConformanceComment
    extra: int

class OverdueFilter(admin.SimpleListFilter):
    title: str
    parameter_name: str
    @beartype
    def lookups(
        self, request: HttpRequest, model_admin: Any
    ) -> tuple[tuple[str, str], ...]: ...
    @beartype
    def queryset(self, request: HttpRequest, queryset: QuerySet) -> QuerySet | None: ...

class ObligationAdminForm(forms.ModelForm):
    recurring_obligation: Incomplete
    inspection: Incomplete
    inspection_frequency: Incomplete
    responsibility: Incomplete
    class Meta:
        model = Obligation
        exclude: Incomplete

    @beartype
    def save(self, commit: bool = True) -> Obligation: ...

class ObligationEvidenceInline(admin.TabularInline):
    model = ObligationEvidence
    extra: int
    fields: Incomplete
    verbose_name: str
    verbose_name_plural: str
    @beartype
    def get_formset(
        self, request: HttpRequest, obj: Obligation | None = None, **kwargs: Any
    ) -> Any: ...

class ObligationAdmin(admin.ModelAdmin):
    form = ObligationAdminForm
    inlines: Incomplete
    list_display: Incomplete
    prepopulated_fields: Incomplete
    fieldsets: Incomplete
    list_filter: Incomplete
    search_fields: Incomplete
    date_hierarchy: str
    @beartype
    def is_overdue(self, obj: Obligation) -> bool: ...
    @beartype
    def get_queryset(self, request: HttpRequest) -> QuerySet[Obligation]: ...
    @beartype
    def save_model(
        self, request: HttpRequest, obj: Obligation, form: ModelForm, change: bool
    ) -> None: ...
    actions: Incomplete
    @beartype
    def update_recurring_dates(
        self, request: HttpRequest, queryset: QuerySet[Obligation]
    ) -> None: ...
    @beartype
    def get_inlines(
        self, request: HttpRequest, obj: Obligation | None = None
    ) -> list[Any]: ...
