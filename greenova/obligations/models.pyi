import logging
from datetime import date
from typing import Any

from _typeshed import Incomplete
from beartype import beartype
from django.db import models
from obligations.validators import (
    validate_obligation_number as validate_obligation_number,
)
from pb_model.models import ProtoBufMixin

from .obligations_pb2 import ObligationProto as ObligationProto

class ProtoBufMixin: ...

logger: logging.Logger

def get_normalize_frequency(): ...

class Obligation(ProtoBufMixin, models.Model):
    pb_model = ObligationProto
    obligation_number: Incomplete
    project: Incomplete
    primary_environmental_mechanism: Incomplete
    procedure: Incomplete
    environmental_aspect: Incomplete
    custom_environmental_aspect: Incomplete
    obligation: Incomplete
    accountability: Incomplete
    responsible_users: Incomplete
    project_phase: Incomplete
    action_due_date: Incomplete
    close_out_date: Incomplete
    status: Incomplete
    supporting_information: Incomplete
    general_comments: Incomplete
    evidence_notes: Incomplete
    recurring_obligation: Incomplete
    recurring_frequency: Incomplete
    recurring_status: Incomplete
    recurring_forecasted_date: Incomplete
    inspection: Incomplete
    inspection_frequency: Incomplete
    site_or_desktop: Incomplete
    new_control_action_required: Incomplete
    obligation_type: Incomplete
    gap_analysis: Incomplete
    notes_for_gap_analysis: Incomplete
    slug: Incomplete
    created_at: Incomplete
    updated_at: Incomplete
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        ordering: Incomplete
        indexes: Incomplete
        default_permissions: Incomplete

    objects: Incomplete
    guardian: Incomplete
    @beartype
    def calculate_next_recurring_date(self) -> date | None: ...
    @beartype
    def update_recurring_forecasted_date(self) -> bool: ...
    @classmethod
    @beartype
    def get_next_obligation_number(cls) -> str: ...
    @beartype
    def clean(self) -> None: ...
    @beartype
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    @property
    @beartype
    def is_overdue(self) -> bool: ...
    @property
    @beartype
    def responsibility_assignments(self) -> models.QuerySet: ...
    @beartype
    def to_pb(self) -> Any: ...
    @classmethod
    @beartype
    def from_pb(cls, proto: Any) -> Obligation: ...

class ObligationEvidence(models.Model):
    obligation: Incomplete
    file: Incomplete
    uploaded_at: Incomplete
    description: Incomplete
    class Meta:
        ordering: Incomplete
        verbose_name: str
        verbose_name_plural: str

    @beartype
    def file_size(self) -> str: ...

class ComplianceComment(models.Model):
    obligation: Incomplete
    comment: Incomplete
    created_at: Incomplete
    updated_at: Incomplete
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        ordering: Incomplete

class NonConformanceComment(models.Model):
    obligation: Incomplete
    comment: Incomplete
    created_at: Incomplete
    updated_at: Incomplete
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        ordering: Incomplete
