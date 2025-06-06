"""Custom middleware classes for the users app.

This module contains Django middleware classes for user-specific request/response
processing, access control, and profile enforcement. All middleware classes must use
beartype for runtime type checking and follow project coding standards.

Author: Adrian Gallo <agallo@enveng-group.com.au>
License: AGPL-3.0
"""

from beartype import beartype
from django.http import HttpRequest, HttpResponse, HttpResponseBase
from typing import Callable


class UserProfileEnforcementMiddleware:
    """Middleware to enforce user profile completeness on each request.

    This middleware checks if the authenticated user's profile is complete and
    redirects to the profile completion page if necessary.

    Args:
        get_response: The next middleware or view in the chain.
    """

    @beartype
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    @beartype
    def __call__(self, request: HttpRequest) -> HttpResponseBase:
        """Check user profile completeness and redirect if incomplete.

        Args:
            request: The HTTP request object.

        Returns:
            HttpResponseBase: The response object, possibly a redirect or streaming response.
        """
        user = getattr(request, "user", None)
        # Only check for authenticated users and skip for profile completion page
        if user and user.is_authenticated and request.path != "/users/profile/complete/":
            profile = getattr(user, "profile", None)
            if profile is not None and not getattr(profile, "has_completed_profile", False):
                from django.shortcuts import redirect
                from django.contrib import messages
                messages.info(
                    request,
                    "Please complete your profile to continue."
                )
                return redirect("users:profile_complete")
        response = self.get_response(request)
        return response
