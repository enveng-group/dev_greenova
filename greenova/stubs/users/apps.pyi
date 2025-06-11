from django.apps import AppConfig

class UsersConfig(AppConfig):
    name: str
    default_auto_field: str
    def ready(self) -> None: ...
