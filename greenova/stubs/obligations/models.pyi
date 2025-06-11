from _typeshed import Incomplete
from datetime import date
from django.db import models
from responsibility.models import Responsibility as Responsibility
from typing import Any

logger: Incomplete

class Obligation(models.Model):
    obligation_number: Any
    project: Any
    primary_environmental_mechanism: Any
    procedure: Any
    environmental_aspect: Any
    custom_environmental_aspect: Any
    obligation: Any
    accountability: Any
    responsibility: Any
    project_phase: Any
    action_due_date: Any
    close_out_date: Any
    status: Any
    supporting_information: Any
    general_comments: Any
    compliance_comments: Any
    non_conformance_comments: Any
    evidence_notes: Any
    recurring_obligation: Any
    recurring_frequency: Any
    recurring_status: Any
    recurring_forecasted_date: Any
    inspection: Any
    inspection_frequency: Any
    site_or_desktop: Any
    new_control_action_required: Any
    obligation_type: Any
    gap_analysis: Any
    notes_for_gap_analysis: Any
    created_at: Any
    updated_at: Any
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        ordering: Incomplete
        indexes: Incomplete
        app_label: str
    def __str__(self) -> str: ...
    def calculate_next_recurring_date(self) -> date | None: ...
    def update_recurring_forecasted_date(self) -> bool: ...
    @classmethod
    def get_next_obligation_number(cls) -> str: ...
    def clean(self) -> None: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    @property
    def is_overdue(self) -> bool: ...

def update_mechanism_counts_on_save(sender, instance, **kwargs) -> None: ...
def update_mechanism_counts_on_delete(sender, instance, **kwargs) -> None: ...

class ObligationEvidence(models.Model):
    obligation: Any
    file: Any
    uploaded_at: Any
    description: Any
    class Meta:
        ordering: Incomplete
        verbose_name: str
        verbose_name_plural: str
    def __str__(self) -> str: ...
    def file_size(self) -> str: ...

def update_forecasted_date_on_change(sender, instance, **kwargs) -> None: ...
def ensure_obligation_number(sender, instance, **kwargs) -> None: ...
