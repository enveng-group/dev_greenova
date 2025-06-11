from _typeshed import Incomplete
from django.http import HttpRequest
from obligations.models import Obligation
from typing import Any

logger: Incomplete
project_selected: Incomplete
dashboard_data_updated: Incomplete

def handle_project_selection(sender: Any, request: HttpRequest, project_id: str | None, **kwargs: dict[str, Any]) -> None: ...
def restore_dashboard_state(sender: Any, request: HttpRequest, user: Any, **kwargs: dict[str, Any]) -> None: ...
def update_dashboard_data(sender: Any, instance: Obligation, **kwargs: dict[str, Any]) -> None: ...
