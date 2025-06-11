from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    default_auto_field: str
    name: str
    verbose_name: str
    def ready(self) -> None: ...
    def get_app_name(self): ...
