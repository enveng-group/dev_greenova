from _typeshed import Incomplete
from beartype import beartype

from .models import Obligation as Obligation
from .utils import is_obligation_overdue as is_obligation_overdue

logger: Incomplete

@beartype
def send_obligation_reminders() -> None: ...
