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

"""Mixins for company access control in Greenova.

This module provides mixins to ensure users can only access data for companies
that they belong to.
"""


from django.http import HttpRequest, HttpResponse
from .models import CompanyMembership
from django.core.exceptions import PermissionDenied


class CompanyAccessMixin:
    """Mixin to ensure users can only access data for companies they belong to.

    This mixin handles both direct company membership and active_company.
    """

    def dispatch(
        self, request: HttpRequest, *args: tuple, **kwargs: dict,
    ) -> HttpResponse:
        """Check if user has permission to access this view.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            The result of the parent dispatch method if access is granted.

        Raises:
            PermissionDenied: If the user does not have access to the company.

        """
        # Superusers always have access
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # First check if the user is a member of any company (for list views)
        if hasattr(request.user, "companies") and request.user.companies.exists():
            return super().dispatch(request, *args, **kwargs)

        # Otherwise check specific company access (for detail/edit views)
        company_id = kwargs.get("company_id")
        if company_id:
            try:
                # Check if user has direct membership
                CompanyMembership.objects.get(company_id=company_id, user=request.user)
                return super().dispatch(request, *args, **kwargs)
            except CompanyMembership.DoesNotExist:
                pass

        # Finally, check active company from session
        company = getattr(request, "active_company", None)
        if (
            company
            and hasattr(company, "users")
            and company.users.filter(id=request.user.id).exists()
        ):
            return super().dispatch(request, *args, **kwargs)

        # No access granted
        msg = "You do not have access to this company."
        raise PermissionDenied(msg)
