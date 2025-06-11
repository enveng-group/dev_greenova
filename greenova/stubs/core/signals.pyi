from _typeshed import Incomplete

logger: Incomplete
User: Incomplete
theme_preference_changed: Incomplete
navigation_accessed: Incomplete

def log_user_login(_sender, _request, user, **_kwargs) -> None: ...
def log_user_logout(_sender, _request, user, **_kwargs) -> None: ...
def handle_user_update(_sender, instance, created, **_kwargs) -> None: ...
