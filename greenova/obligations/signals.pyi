from _typeshed import Incomplete
from beartype import beartype

from .models import Obligation as Obligation

logger: Incomplete

@beartype
def validate_custom_aspect(sender, instance: Obligation, **kwargs) -> None: ...
@beartype
def update_forecasted_date_after_save(
    sender, instance: Obligation, created: bool, **kwargs
) -> None: ...
@beartype
def log_after_save_obligation(
    sender, instance: Obligation, created: bool, **kwargs
) -> None: ...
@beartype
def log_after_delete_obligation(sender, instance: Obligation, **kwargs) -> None: ...
