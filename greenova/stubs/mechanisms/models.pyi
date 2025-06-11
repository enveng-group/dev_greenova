from _typeshed import Incomplete
from builtins import property as property
from core.types import StatusData
from django.db import models
from django_matplotlib.fields import MatplotlibFigureField

logger: Incomplete

class EnvironmentalMechanism(models.Model):
    name: models.CharField
    project: models.ForeignKey
    description: models.TextField
    category: models.CharField
    reference_number: models.CharField
    effective_date: models.DateField
    status: models.CharField
    not_started_count: models.IntegerField
    in_progress_count: models.IntegerField
    completed_count: models.IntegerField
    overdue_count: models.IntegerField
    primary_environmental_mechanism: models.CharField
    created_at: models.DateTimeField
    updated_at: models.DateTimeField
    status_chart: MatplotlibFigureField
    class Meta:
        verbose_name: str
        verbose_name_plural: str
        ordering: list[str]
    def __str__(self) -> str: ...
    @property
    def total_obligations(self) -> int: ...
    def update_obligation_counts(self) -> None: ...
    def get_status_data(self) -> StatusData: ...

def update_all_mechanism_counts() -> int: ...
