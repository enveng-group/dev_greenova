from django.apps import AppConfig

class ProtobufConfig(AppConfig):
    default_auto_field: str
    name: str
    verbose_name: str
    def ready(self) -> None: ...
