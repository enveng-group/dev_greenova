from beartype import beartype
from django.apps import AppConfig

class ObligationsConfig(AppConfig):
    default_auto_field: str
    name: str
    @beartype
    def ready(self) -> None: ...
