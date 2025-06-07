from typing import Any

from _typeshed import Incomplete
from django.db import models

logger: Incomplete

class EnvironmentalMechanism(models.Model):
    name: Incomplete
    project: Incomplete
    description: Incomplete
    category: Incomplete
    reference_number: Incomplete
    effective_date: Incomplete
    status: Incomplete
    not_started_count: Incomplete
    in_progress_count: Incomplete
    completed_count: Incomplete
    overdue_count: Incomplete
    primary_environmental_mechanism: Incomplete
    created_at: Incomplete
    updated_at: Incomplete
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        ordering: list[str]
        default_permissions: Incomplete

    @property
    def total_obligations(self) -> int: ...
    def update_obligation_counts(self) -> None: ...
    def get_status_data(self) -> dict[str, Any]: ...
    def save(self, *args: object, **kwargs: object) -> None: ...

def update_all_mechanism_counts() -> int: ...
