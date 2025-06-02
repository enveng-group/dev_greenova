from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self) -> None:
        pass  # Signal connection is handled at the top level
