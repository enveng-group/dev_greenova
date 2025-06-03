"""Copyright (C) 2025 Adrian Gallo.

This file is part of Greenova.

Greenova is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Greenova is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Greenova. If not, see <https://www.gnu.org/licenses/>.

Author: Adrian Gallo <agallo@enveng-group.com.au>
"""

"""Module for API views that handle bulk operations on obligations."""

from models import Obligation
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.utils.decorators import method_decorator
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from beartype import beartype
from typing import TYPE_CHECKING, Any, cast
import json
import logging


if TYPE_CHECKING:
    UserModel = AbstractUser
else:
    UserModel = get_user_model()

logger = logging.getLogger(__name__)

# Properly define UserType as a TypeAlias for mypy
type UserType = AbstractUser


@beartype
def _get_validated_user(
    request: HttpRequest,
) -> tuple[UserType, None] | tuple[None, JsonResponse]:
    """Authenticate and authorize the user, ensuring they are a superuser.

    Args:
        request: The HTTP request.

    Returns:
        A tuple containing the user instance and None if successful,
        or None and a JsonResponse if authentication/authorization fails.

    """
    if not request.user.is_authenticated:
        return None, JsonResponse({"error": "Authentication required"}, status=401)

    # Use the defined UserType alias in the cast
    user_instance = cast("UserType", request.user)

    if not user_instance.is_superuser:
        return None, JsonResponse(
            {"error": "Permission denied. Superuser access required."}, status=403,
        )
    return user_instance, None


@beartype
def _parse_and_validate_ids_from_request(
    request: HttpRequest,
) -> tuple[list[str | int], None] | tuple[None, JsonResponse]:
    """Parse and validate 'ids' from the JSON request body.

    Args:
        request: The HTTP request.

    Returns:
        A tuple containing the list of IDs and None if successful,
        or None and a JsonResponse if validation fails or body is invalid.

    """
    if not request.body:
        return None, JsonResponse({"error": "Empty request body"}, status=400)
    try:
        # Type cast the json.loads result to dict[str, Any] for mypy
        data: dict[str, Any] = cast(
            "dict[str, Any]", json.loads(request.body.decode("utf-8")))
    except json.JSONDecodeError:
        logger.warning("Failed to decode JSON from request body.", exc_info=True)
        return None, JsonResponse({"error": "Invalid JSON payload"}, status=400)
    except UnicodeDecodeError:
        logger.warning("Failed to decode request body as UTF-8.", exc_info=True)
        return None, JsonResponse({"error": "Invalid request encoding"}, status=400)

    ids = data.get("ids", [])
    if not (
        isinstance(ids, list)
        and ids
        and all(isinstance(item, str | int) for item in ids)
    ):
        return None, JsonResponse(
            {
                "error": (
                    "Invalid payload: 'ids' must be a non-empty list of"
                    " strings or integers."
                ),
            },
            status=400,
        )
    return ids, None


@method_decorator(csrf_exempt, name="dispatch")
class MarkObligationsCompleteAPI(View):
    """API endpoint to mark obligations as complete in bulk."""

    @beartype
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """Initialize the MarkObligationsCompleteAPI view.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().__init__(*args, **kwargs)

    @beartype
    def post(self, request: HttpRequest, *args: tuple, **kwargs: dict) -> JsonResponse:
        """API endpoint to mark obligations as complete in bulk.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse indicating success or failure.

        """
        user, error_response = _get_validated_user(request)
        if error_response is not None:
            return error_response

        ids, error_response = _parse_and_validate_ids_from_request(request)
        if error_response is not None:
            return error_response

        try:
            updated_count: int = Obligation.objects.filter(
                obligation_number__in=ids,
            ).update(status="Complete")

            logger.info(
                "User %s marked %d obligations as complete. IDs: %s",
                user.pk,
                updated_count,
                ids,
            )

            return JsonResponse(
                {
                    "message": f"{updated_count} obligations marked as complete.",
                    "updated_ids": ids,
                },
                status=200,
            )
        except Exception as exc:  # pylint: disable=broad-except
            logger.error(
                "Error in mark_complete API for user %s, IDs %s: %s",
                user.pk if user else "Unknown",
                ids or "Unknown",
                exc,
                exc_info=True,
            )
            return JsonResponse({"error": "Server error"}, status=500)


@method_decorator(csrf_exempt, name="dispatch")
class DeleteObligationsAPI(View):
    """API endpoint to delete obligations in bulk."""

    @beartype
    def __init__(self, *args: tuple, **kwargs: dict) -> None:
        """Initialize the DeleteObligationsAPI view.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        """
        super().__init__(*args, **kwargs)

    @beartype
    def delete(
            self,
            request: HttpRequest,
            *args: tuple,
            **kwargs: dict) -> JsonResponse:
        """API endpoint to delete obligations in bulk.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            JsonResponse indicating success or failure.

        """
        user, error_response = _get_validated_user(request)
        if error_response is not None:
            return error_response

        ids, error_response = _parse_and_validate_ids_from_request(request)
        if error_response is not None:
            return error_response

        try:
            deleted_count: int = Obligation.objects.filter(
                obligation_number__in=ids,
            ).update(status="Deleted")

            logger.info(
                "User %s marked %d obligations as deleted. IDs: %s",
                user.pk,
                deleted_count,
                ids,
            )

            return JsonResponse(
                {
                    "message": f"{deleted_count} obligations marked as deleted.",
                    "deleted_ids": ids,
                },
                status=200,
            )
        except Exception as exc:  # pylint: disable=broad-except
            logger.error(
                "Error in delete API for user %s, IDs %s: %s",
                user.pk if user else "Unknown",
                ids or "Unknown",
                exc,
                exc_info=True,
            )
            return JsonResponse({"error": "Server error"}, status=500)
