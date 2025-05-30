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

"""Management command to ensure the default TBA company exists.

This module defines a custom Django management command for ensuring the default
company with ID 1 exists in the database for the company app.
"""


from company.models import Company
from django.core.management.base import BaseCommand
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    """Custom management command to ensure the default TBA company exists."""

    help = "Ensures the default TBA company with ID 1 exists"

    def handle(self, *args: object, **options: object) -> None:
        """Execute the command to ensure the default TBA company exists.

        Args:
            *args: Variable length argument list.
            **options: Arbitrary keyword arguments.

        """
        _, created = Company.objects.get_or_create(
            id=1,
            defaults={
                "name": "TBA",
                "description": "Default company for unassigned items",
                "company_type": "other",
                "is_active": True,
            },
        )

        if created:
            self.stdout.write(
                self.style.SUCCESS("Created default TBA company with ID 1"),
            )
        else:
            self.stdout.write(self.style.SUCCESS("Default TBA company already exists"))

        # Removed project-related code as the relationship has been removed
