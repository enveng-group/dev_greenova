# Stub file for obligations.utils
from datetime import date
from typing import TYPE_CHECKING, Any, Dict, Optional, Union

if TYPE_CHECKING:
    from .models import Obligation

def is_obligation_overdue(
    obligation: Union["Obligation", Dict[str, Any]],
    reference_date: Optional[date] = None,
) -> bool: ...
def get_obligation_status(obligation: Any) -> str: ...
def normalize_frequency(frequency: str) -> str: ...
def get_responsibility_display_name(responsibility_value: str) -> str: ...
