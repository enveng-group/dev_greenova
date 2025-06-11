from _typeshed import Incomplete
from collections.abc import Sequence
from dataclasses import dataclass
from django.db.models import QuerySet
from models import EnvironmentalMechanism as EnvironmentalMechanism
from obligations.models import Obligation

logger: Incomplete

@dataclass
class ObligationInsightParams:
    mechanism_id: int
    status: str
    status_key: str
    obligations: Sequence[Obligation]
    total_count: int
    error: str | None = ...

def serialize_obligation_insights(params: ObligationInsightParams) -> ObligationInsightResponse: ...
def serialize_mechanism_chart_data(mechanism: EnvironmentalMechanism) -> ChartData: ...
def serialize_overall_chart_data(project_id: int, mechanisms: QuerySet) -> ChartData: ...
def serialize_chart_response(charts: list[ChartData], error: str | None = None) -> ChartResponse: ...
def status_string_to_enum(status: str) -> ObligationStatus: ...
def status_enum_to_string(status: ObligationStatus) -> str: ...
