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

"""Middleware for attaching the active company to the request object.

This module provides middleware to manage the active company context for
authenticated users in the Greenova company app.
"""


from django.http import HttpRequest
import logging
from .models import Company
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(__name__)


class ActiveCompanyMiddleware(MiddlewareMixin):
    """Middleware to attach the active company to the request object.

    If the user is authenticated, it retrieves the active company ID from the session.
    If the company exists, it is attached to the request. Otherwise, it logs an error
    and sets the active company to None. Additionally, it checks if the user is a member
    of the company and handles cases where they are not.
    """

    def process_request(self, request: HttpRequest) -> None:
        """Attach the active company to the request if the user is authenticated.

        Args:
            request: The HTTP request object.

        """
        if request.user.is_authenticated:
            active_company_id = request.session.get("active_company_id")
            if active_company_id:
                try:
                    company = Company.objects.get(id=active_company_id)
                    if request.user not in company.users.all():
                        logger.warning(
                            "User %s is not a member of company %s.",
                            request.user,
                            company,
                        )
                        request.active_company = None
                    else:
                        request.active_company = company
                except Company.DoesNotExist:
                    logger.exception(
                        "Active company with ID %s does not exist.",
                        active_company_id,
                    )
                    request.active_company = None
            else:
                request.active_company = None
        else:
            request.active_company = None
