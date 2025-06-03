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

"""Utility functions for user-related operations.

This module provides helper functions to calculate and manage
user-specific data, such as overdue obligations.

Module namespace: users.utils
"""

from company.models import CompanyMembership
from obligations.models import Obligation
from projects.models import Project


def calculate_overdue_obligations(user_id: int) -> list[Obligation]:
    """Calculate overdue obligations for a given user."""
    company_memberships = CompanyMembership.objects.filter(user_id=user_id)
    user_roles = company_memberships.values_list("role", flat=True).distinct()
    project_ids = Project.objects.filter(members=user_id).values_list("id", flat=True)
    obligations = (
        Obligation.objects.filter(
            responsibility__in=user_roles, project_id__in=project_ids,
        )
        .select_related("project")
        .distinct()
    )
    return [obligation for obligation in obligations if obligation.is_overdue]
