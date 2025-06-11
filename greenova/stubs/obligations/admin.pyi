from .models import Obligation, ObligationEvidence
from _typeshed import Incomplete
from django import forms
from django.contrib import admin
from django.db.models import QuerySet
from django.forms import ModelForm
from django.http import HttpRequest

logger: Incomplete

class OverdueFilter(admin.SimpleListFilter):
    title: str
    parameter_name: str
    def lookups(self, request, model_admin): ...
    def queryset(self, request, queryset): ...

class ObligationAdminForm(forms.ModelForm):
    recurring_obligation: Incomplete
    inspection: Incomplete
    inspection_frequency: Incomplete
    responsibility: Incomplete
    class Meta:
        model = Obligation
        fields: Incomplete
    def save(self, commit: bool = True): ...

class ObligationEvidenceInline(admin.TabularInline):
    model = ObligationEvidence
    extra: int
    fields: Incomplete
    verbose_name: str
    verbose_name_plural: str
    def get_formset(self, request, obj: Incomplete | None = None, **kwargs): ...

class ObligationAdmin(admin.ModelAdmin):
    form = ObligationAdminForm
    inlines: Incomplete
    list_display: Incomplete
    fieldsets: Incomplete
    list_filter: Incomplete
    search_fields: Incomplete
    date_hierarchy: str
    def is_overdue(self, obj): ...
    def get_queryset(self, request: HttpRequest) -> QuerySet[Obligation]: ...
    def save_model(self, request: HttpRequest, obj: Obligation, form: ModelForm, change: bool) -> None: ...
    actions: Incomplete
    def update_recurring_dates(self, request, queryset) -> None: ...
    def get_inlines(self, request, obj: Incomplete | None = None): ...
