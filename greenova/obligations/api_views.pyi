from _typeshed import Incomplete
from beartype import beartype
from django.contrib.auth import get_user_model as get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views import View

UserModel = AbstractUser
logger: Incomplete
type UserType = AbstractUser

class ObligationBulkAPI(View):
    def options(self, request: HttpRequest, *args, **kwargs) -> HttpResponse: ...

class MarkObligationsCompleteAPI(View):
    @beartype
    def __init__(self, *args: tuple, **kwargs: dict) -> None: ...
    @beartype
    def post(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> JsonResponse: ...

class DeleteObligationsAPI(View):
    @beartype
    def __init__(self, *args: tuple, **kwargs: dict) -> None: ...
    @beartype
    def delete(
        self, request: HttpRequest, *args: tuple, **kwargs: dict
    ) -> JsonResponse: ...
