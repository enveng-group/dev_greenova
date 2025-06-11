from _typeshed import Incomplete
from beartype import beartype
from django.contrib.auth import get_user_model as get_user_model
from django.contrib.auth.models import AbstractUser
from django.http import HttpRequest, JsonResponse
from django.views import View

UserModel = AbstractUser
logger: Incomplete
type UserType = AbstractUser

@beartype
def _get_validated_user(request: HttpRequest) -> tuple[UserType, None] | tuple[None, JsonResponse]: ...
@beartype
def _parse_and_validate_ids_from_request(request: HttpRequest) -> tuple[list[str | int], None] | tuple[None, JsonResponse]: ...

class MarkObligationsCompleteAPI(View):
    @beartype
    def __init__(self, *args: tuple, **kwargs: dict) -> None: ...
    @beartype
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> JsonResponse: ...

class DeleteObligationsAPI(View):
    @beartype
    def __init__(self, *args: tuple, **kwargs: dict) -> None: ...
    @beartype
    def delete(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> JsonResponse: ...
