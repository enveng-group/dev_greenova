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
from .permissions import user_can_view_company
from beartype import beartype


class CompanyAccessMixin:
    """Mixin to ensure users can only access data for companies they belong to.

    This mixin handles both direct company membership and active_company.
    """

    @beartype
    def dispatch(
        self, request: HttpRequest, *args: tuple, **kwargs: dict,
    ) -> HttpResponse:
        company_id = kwargs.get("company_id")
        if company_id:
            company = CompanyMembership.objects.filter(
                company_id=company_id, user=request.user
            ).first()
            if company and user_can_view_company(request.user, company):
                return super().dispatch(request, *args, **kwargs)
        # Fallback: check active company
        company = getattr(request, "active_company", None)
        if company and user_can_view_company(request.user, company):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied("You do not have access to this company.")
