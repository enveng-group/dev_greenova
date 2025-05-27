"""
Management command to ensure the default TBA company exists.

This module defines a custom Django management command for ensuring the default
company with ID 1 exists in the database for the company app.
"""

import logging

from company.models import Company
from django.core.management.base import BaseCommand

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
                self.style.SUCCESS("Created default TBA company with ID 1")
            )
        else:
            self.stdout.write(self.style.SUCCESS("Default TBA company already exists"))

        # Removed project-related code as the relationship has been removed
